import socket

print("socket server started:")
print("waiting for connection:")

server_socket=socket.socket()
port=12345

server_socket.bind(('',port))
server_socket.listen(5)

client_socket, client_addr = server_socket.accept()
client_socket.sendall('Thank you for connecting'.encode())

print("Client connected.")

working=True
while working:
    client_data=client_socket.recv(1024).decode()
    if not client_data:
        print("Client disconnected")
        working = False
        client_socket.close()
    else:
        answer_message="Your message: "+client_data
        client_socket.sendall(answer_message.encode())
        print(client_data)
        if client_data=="exit":
            print("Exiting")
            working=False
            client_socket.close()