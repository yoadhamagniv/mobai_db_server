import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 6969        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'200#TestCamera#1643810131#1643811180')
    data = s.recv(4096)
    print('Received', data)
    s.sendall(b'100#OK')