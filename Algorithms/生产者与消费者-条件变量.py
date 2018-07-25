# coding=utf-8

import threading
import time

class Producer(threading.Thread):
    def run(self):
        global count
        while True:
            if con.acquire():
                if count > 1000:
                    con.wait()
                else:
                    count += 100
                    msg = self.name + " produce 100, count=" + str(count)
                    print msg
                    con.notify()
                con.release()
            time.sleep(1)


class Consumer(threading.Thread):
    def run(self):
        global count
        while True:
            if con.acquire():
                if count < 100:
                    con.wait()
                else:
                    count -= 3
                    msg = self.name + " consume 3, count=" + str(count)
                    print msg
                    con.notify()
                con.release()
            time.sleep(1)

if __name__ == "__main__":
    count = 500
    con = threading.Condition()

    for i in range(2):
        p = Producer()
        p.start()

    for i in range(5):
        c = Consumer()
        c.start()        