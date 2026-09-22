import socket

print("socket server started:")

soc=socket.socket()
port=12345

soc.bind(('',port))
soc.listen(5)

while True:
    c, addr=soc.accept()
    c.send('Thank you for connecting'.encode())
    print(c.recv(1024).decode())
    c.close()