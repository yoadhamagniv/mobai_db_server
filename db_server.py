from firebase_handler import *
import socket
import threading

ENDFIX = '&'

class db_server(object):
    def __init__(self, host, port, db):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.db = db

    def start(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            threading.Thread(target = self.handleClient,args = (client,address)).start()
            print(f"new client - {address}\n")

    def handleClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size).decode("utf-8")
                data = data.split('#')
                print(data)
                if data[0]=="200": #asking for schedule in timespan
                    response = get_schedule_for_time_span(data[1],int(data[2]),int(data[3]),self.db)
                    client.sendall((str(response)+ ENDFIX).encode('utf-8')) #{'Sleep': [('1643810131', 1643810156), ('1643810162', 1643810193)], 'Awake': [('1643810156', 1643810162)]}
                elif data[0]=="250": #checks if username exists
                    response = is_username_valid(data[1],self.db)
                    client.sendall((str(response)+ ENDFIX).encode('utf-8')) #YES or NO
                elif data[0]=="275": #checks if username and password match
                    response = does_password_match(data[1],data[2],self.db)
                    client.sendall((str(response)+ ENDFIX).encode('utf-8')) #YES or NO
                elif data[0]=="300": #wanting to sign up
                    response = add_user(data[1],data[2],data[3],data[4],data[5],self.db) #camera_id, password, email, baby_birthdate, babyname, db
                    client.sendall((str(response)+ ENDFIX).encode('utf-8')) #OK or FAILED
                elif data[0]=="350": #asking for current state
                    response = get_curr_state(data[1],self.db) #camera_id, db
                    client.sendall((str(response) + ENDFIX).encode('utf-8') + ENDFIX)#{'start_time': 1643813869, 'state': 'Sleep'}
            except Exception as e:
                print(e)
                client.sendall(("error" + ENDFIX).encode('utf-8') + ENDFIX)
                return False



if __name__ == '__main__':
    PORT = 6969
    cred = credentials.Certificate("mobaitestdata-firebase-adminsdk-qknjq-7204e01919.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    if not (try_open_db(db)): quit()
    db_server('10.0.0.11', PORT, db).start()

# 200#{cameraId}#{time1}#{time2}