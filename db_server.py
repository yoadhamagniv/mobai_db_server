from firebase_handler import *
import socket
import threading



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
                #print(data)
                if data[0]=="200": #asking for schedule in timespan
                    while True:
                        response = get_schedule_for_time_span(data[1],int(data[2]),int(data[3]),self.db)
                        client.sendall(str(response).encode('utf-8')) #{'Sleep': [('1643810131', 1643810156), ('1643810162', 1643810193)], 'Awake': [('1643810156', 1643810162)]}
                        data = client.recv(size).decode("utf-8").split('#')
                        if data[0] == "100":
                            break
                if data[0]=="250": #checks if username exists
                    while True:
                        response = does_username_exist(data[1],self.db)
                        client.sendall(str(response).encode('utf-8')) #YES or NO
                        data = client.recv(size).decode("utf-8").split('#')
                        if data[0] == "100":
                            break
                if data[0]=="275": #checks if username and password match
                    while True:
                        response = does_password_match(data[1],data[2],self.db)
                        client.sendall(str(response).encode('utf-8')) #YES or NO
                        data = client.recv(size).decode("utf-8").split('#')
                        if data[0] == "100":
                            break
                if data[0]=="300": #wanting to sign up
                    while True:
                        response = add_user(data[1],data[2],data[3],data[4],data[5],data[6],self.db) #camera_id, password, email, baby_birthdate, babyname, db
                        client.sendall(str(response).encode('utf-8')) #OK or FAILED
                        data = client.recv(size).decode("utf-8").split('#')
                        if data[0] == "100":
                            break
                if data[0]=="350": #asking for current state
                    while True:
                        response = get_curr_state(data[1],self.db) #camera_id, db
                        client.sendall(str(response).encode('utf-8'))#{'start_time': 1643813869, 'state': 'Sleep'}
                        data = client.recv(size).decode("utf-8").split('#')
                        if data[0] == "100":
                            break
            except:
                client.close()
                return False



if __name__ == '__main__':
    PORT = 6969
    cred = credentials.Certificate("mobaitestdata-firebase-adminsdk-qknjq-7204e01919.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    if not (try_open_db(db)): quit()
    db_server('127.0.0.1', PORT, db).start()

# 200#{cameraId}#{time1}#{time2}