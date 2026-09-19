import asyncio
import time
from timeit import default_timer as timer


class async_class():

    log=""

    def __init__(self, pause_value: int = 1):
        self.pause_value=pause_value
        print(f"Class init {pause_value} sec OK")

    async def do_something(self):
        print("Start 1st")
        await asyncio.sleep(self.pause_value+5)
        print("Done 1st")
        self.log=self.log+"Done 1st"

    async  def do_something2(self):
        print("Start 2st")
        await asyncio.sleep(self.pause_value)
        print("Done 2st")
        self.log = self.log + "Done 2st"

async def main():

    ########### MAIN ACTION

    my_async=async_class(3)

    task1 = asyncio.create_task(my_async.do_something())
    task2 = asyncio.create_task(my_async.do_something2())

    await task1
    await task2

    print("Main job is done")
    print("Log: "+my_async.log)

    ###########


start_time = time.time()
start_time1 = timer()

asyncio.run(main())

end_time = time.time()
end_time1 = timer()

print(f"Time: Total runtime of the program is {end_time - start_time} seconds")
print(f"timer: Total runtime of the program is {end_time1 - start_time1} seconds")
