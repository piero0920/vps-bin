import time
import threading
from datetime import timedelta

class ElapsedTimeThread(threading.Thread):
    def __init__(self):
        super(ElapsedTimeThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        thread_start = time.time()
        while not self.stopped():
            hours, rem = divmod(time.time()-thread_start, 3600)
            minutes, seconds = divmod(rem, 60)
            print("\rElapsed {:0>2}h:{:0>2}m:{:05.2f}s".format(int(hours),int(minutes),seconds), end="")
            time.sleep(0.01)

if __name__ == "__main__":
    start = time.time()
    thread = ElapsedTimeThread()
    thread.start()
    # do something
    for i in range(3):
        time.sleep(5)
        print()
        print(f'{i}/3 - first job')
        print('    sssss')
        print()
        print('    ssada')
    # something is finished so stop the thread
    thread.stop()
    thread.join()
    print() # empty print() to output a newline
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Finished in {:0>2}h:{:0>2}m:{:05.2f}s".format(int(hours),int(minutes),seconds))
    #print("Finished in {} minutes".format((round((time.time()-start)/60, 2))))