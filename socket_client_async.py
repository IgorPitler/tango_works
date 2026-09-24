import socket
import asyncio

print("Socket client:")

# seconds
operation_timeout = 200

camserver_ip = "127.0.0.1"
camserver_port = 12345

try:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # operation timeout in seconds
    soc.settimeout(operation_timeout)
except Exception as e:
    print(f"Error creating socket {e}")

try:
    soc.connect((camserver_ip, camserver_port))
    ans = soc.recv(1024).decode()
    print("Connection answer: " + ans)
except Exception as e:
    print(f"Socket connection error {e}")

### MAIN

try:
    command="test1"
    soc.sendall(command.encode())
    # print server answer
    ans = soc.recv(1024).decode()
    print("Answer: " + ans)

    command="test2"
    soc.sendall(command.encode())
    # print server answer
    ans = soc.recv(1024).decode()
    print("Answer: " + ans)

    command="test3"
    soc.sendall(command.encode())
    # print server answer
    ans = soc.recv(1024).decode()
    print("Answer: " + ans)

    #command="exit"
    #soc.sendall(command.encode())
    #print server answer
    #ans = soc.recv(1024).decode()
    #print("Answer: " + ans)

except Exception as e:
    print("Error sending command")

### FINISH...

try:
    soc.shutdown(socket.SHUT_RDWR)
except Exception as e:
    print("Error shutdown socket")

# use AFTER shutdown
try:
    soc.close()
except Exception as e:
    print("Error closing socket")

class async_socket:

    def __init__(self):
        pass

    async def connect(self):
        pass

    async def message(self, message_text):
        pass

    async def close(self):
        pass

async def main():
    mysoc=async_socket()
    await mysoc.connect()
    await mysoc.message("test1")
    await mysoc.message("test2")
    await mysoc.message("test3")
    await mysoc.close()

asyncio.run(main())