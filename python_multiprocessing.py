import multiprocessing
import time


class multi_demo:

    working=0

    def __init__(self):
        pass

    def process_actions(self):
        print("Process action started.")
        time.sleep(3)
        print("Process actions OK.")


    def run_process(self):

        self.proc1=multiprocessing.Process(target=self.process_actions)
        self.proc1.start()

    def close(self):
        self.proc1.close()

if __name__ == "__main__":

    print("Multiprocessing test:")

    m1=multi_demo()
    m1.run_process()

    print("Main finished.")