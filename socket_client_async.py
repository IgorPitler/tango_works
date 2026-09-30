import socket
import asyncio

import time
from timeit import default_timer as timer


print("Async Socket client:")

class async_socket:

    data=""
    # seconds
    #operation_timeout = 200

    def __init__(self, camserver_ip : str ="", camserver_port : int =12345 ):
        self.writer = None
        self.reader = None
        self.camserver_ip=camserver_ip
        self.camserver_port=camserver_port

    async def connect(self):
        try:
            print("Connecting...")
            self.reader, self.writer = await asyncio.open_connection(self.camserver_ip, self.camserver_port)
            data = await self.reader.read(1000)
            print(f'Connect : Received: {data.decode()!r}')
        except Exception as e:
            print(f"Connect error {e}")


    async def send_command(self, message_text : str) -> str:
        try:
            print("Requesting... "+message_text)
            self.writer.write(message_text.encode())
            await self.writer.drain()

            data = await self.reader.read(1000)
            #print(f'Received: {data.decode()!r}')
            return data.decode()
        except Exception as e:
            print("Error sending command")
            return ""

    async def close(self):
        try:
            print("Closing connection")
            self.writer.close()
            await self.writer.wait_closed()
        except Exception as e:
            print("Closing error")


async def main():
    mysoc=async_socket("127.0.0.1", 12345)
    await mysoc.connect()
    ans=await mysoc.send_command("test1")
    print("Answer: "+ans)
    print("1-2")
    ans=await mysoc.send_command("test2")
    print("Answer: "+ans)
    print("2-3")
    ans=await mysoc.send_command("test3")
    print("Answer: "+ans)
    await mysoc.close()

start_time = time.time()
start_time1 = timer()

asyncio.run(main())

end_time = time.time()
end_time1 = timer()

print(f"Time: Total runtime of the program is {end_time - start_time} seconds")
print(f"timer: Total runtime of the program is {end_time1 - start_time1} seconds")