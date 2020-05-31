import json
import socket
import time

SERVER_MAC = 'B8:27:EB:87:5B:87'
PORT = 3
BACKLOG = 1
SIZE = 1024

s = socket.socket(socket.AF_BLUETOOTH, 
                  socket.SOCK_STREAM, 
                  socket.BTPROTO_RFCOMM)
s.setblocking(False)
for i in range(300):
    try:
        s.connect((SERVER_MAC, PORT))
        break
    except:
        s.close()
        time.sleep(0.11111111)

text = "Hello Igor"
s.send(bytes(text, 'UTF-8'))
data = s.recv(SIZE)
print(data)
s.close()

