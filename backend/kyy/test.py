import socket
import send_data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 80
s.connect(('115.21.152.84', port))

s.send(send_data.send_msg[port])
print(s.recv(4096))