# -*- coding: utf-8 -*-

import time
from threading import Thread, Condition


class Producer(Thread):
    def run(self):
        global count
        while True:
            if condition.acquire():
                if count > 1000:
                    condition.wait()
                else:
                    count += 100
                    print self.name + " prudce 100, count = " + str(count)
                    condition.notify()
                condition.release()
            time.sleep(1)


class Consumer(Thread):
    def run(self):
        global count
        while True:
            if condition.acquire():
                if count < 100:
                    condition.wait()
                else:
                    count -= 3
                    print self.name + " Consumer 3, count = " + str(count)
                    condition.notify()
                condition.release()
            time.sleep(1)


if __name__ == "__main__":
    count = 500
    condition = Condition()

    for _ in range(2):
        producer = Producer()
        producer.start()

    for _ in range(5):
        consumer = Consumer()
        consumer.start()
