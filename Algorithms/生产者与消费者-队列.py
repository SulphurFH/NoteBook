# coding=utf-8

import threading
import time
from Queue import Queue

class Producer(threading.Thread):
    def run(self):
        global queue
        count = 0
        while True:
            if queue.qsize() < 1000:
                for i in range(100):
                    count += 1
                    msg = 'produce ' + str(count)
                    queue.put(msg)
                    print msg
        time.sleep(1)

class Customer(threading.Thread):
    def run(self):
        global queue
        while True:
            if queue.qsize() > 100:
                for i in range(3):
                    msg = self.name + " custome " + queue.get()
                    print msg
        time.sleep(1)


if __name__ == "__main__":
    queue = Queue()

    for i in range(500):
        queue.put('initial ' + str(i))

    for i in range(3):
        p = Producer()
        p.start()

    for i in range(5):
        c = Customer()
        c.start()