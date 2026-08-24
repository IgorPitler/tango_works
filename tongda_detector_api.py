#from urllib import response

import socket

# restful edition
class detector_api:

    detector_ip="127.0.0.1"

    def __init__(self):
        pass

    def init_detector(self):
        pass

print("Socket client example:")

soc=socket.socket()
soc.connect(('127.0.0.1', 12345))
# print server welcome message
print(soc.recv(1024).decode())
# send sample string to socket
soc.send(b'Hello World')
soc.close()


