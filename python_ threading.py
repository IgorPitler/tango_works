import threading
import time

print("Threading demo:")

def task():
    print('thread is running...')
    time.sleep(3)
    print('thread is over...')

thread= threading.Thread(target=task)
print(f'Thread created: {thread.name}')
thread.start()
#thread.join()
print("Main finished")
