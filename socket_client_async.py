import socket
import asyncio

import time

print("Socket client:")

class async_socket:

    # seconds
    operation_timeout = 200

    camserver_ip = "127.0.0.1"
    camserver_port = 12345

    def __init__(self):
        pass

    async def connect(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # operation timeout in seconds
            self.soc.settimeout(self.operation_timeout)
        except Exception as e:
            print(f"Error creating socket {e}")

        try:
            self.soc.connect((self.camserver_ip, self.camserver_port))
            ans = self.soc.recv(1024).decode()
            print("Connection answer: " + ans)
        except Exception as e:
            print(f"Socket connection error {e}")

    async def message(self, message_text : str):

        try:
            command = message_text
            self.soc.sendall(command.encode())
            # print server answer
            ans = self.soc.recv(1024).decode()
            print("Answer: " + ans)

        except Exception as e:
            print("Error sending command")

    async def close(self):
        try:
            self.soc.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print("Error shutdown socket")

        # use AFTER shutdown
        try:
            self.soc.close()
        except Exception as e:
            print("Error closing socket")

async def main():
    mysoc=async_socket()
    await mysoc.connect()
    await mysoc.message("test1")
    await mysoc.message("test2")
    await mysoc.message("test3")
    await mysoc.close()

asyncio.run(main())