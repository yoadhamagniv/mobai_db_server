import socket
import datetime

HOST = '172.23.160.1'  # The server's hostname or IP address
PORT = 6969        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'200#TestCamera#1102846320#1645870320')
    #s.sendall(b'350#TestCamera')
    data = s.recv(2*2*8192)
    print('Received', data)
    s.sendall(b'100#OK')