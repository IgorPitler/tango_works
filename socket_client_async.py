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

        except Exception as e:
            print(f"Connect error {e}")



    async def message(self, message_text : str):

        try:


        except Exception as e:
            print("Error sending command")

    async def close(self):
        try:

        except Exception as e:
            print("Closing error")


async def main():
    mysoc=async_socket()
    await mysoc.connect()
    await mysoc.message("test1")
    await mysoc.message("test2")
    await mysoc.message("test3")
    await mysoc.close()

asyncio.run(main())