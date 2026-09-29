import socket
import asyncio

import time

print("Async Socket client:")

class async_socket:

    # seconds
    operation_timeout = 200


    def __init__(self, camserver_ip : str ="", camserver_port : int =12345 ):
        self.writer = None
        self.reader = None
        self.camserver_ip=camserver_ip
        self.camserver_port=camserver_port

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.camserver_ip, self.camserver_port)
        except Exception as e:
            print(f"Connect error {e}")


    async def send_command(self, message_text : str):
        try:
            self.writer.write(message_text.encode())
            await self.writer.drain()

            data = await self.reader.read(2000)
            print(f'Received: {data.decode()!r}')
            return data.decode()
        except Exception as e:
            print("Error sending command")
            return ""

    async def close(self):
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except Exception as e:
            print("Closing error")


async def main():
    mysoc=async_socket("127.0.0.1", 12345)
    await mysoc.connect()
    ans=await mysoc.send_command("test1")
    #print(ans)
    print("1-2")
    ans=await mysoc.send_command("test2")
    #print(ans)
    print("2-3")
    ans=await mysoc.send_command("test3")
    #print(ans)
    await mysoc.close()

asyncio.run(main())