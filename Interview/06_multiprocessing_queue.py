# -*- coding: utf-8 -*-

import time
import random
from multiprocessing import Process, Queue


def wirter(q):
    for value in ['A', 'B', 'C']:
        print 'Put %s to queue...' % value
        q.put(value)
        time.sleep(random.random())


def reader(q):
    while True:
        if not q.empty():
            value = q.get(True)
            print 'Get %s from queue.' % value
            time.sleep(random.random())
        else:
            break


if __name__ == "__main__":
    q = Queue()
    process_wirter = Process(target=wirter, args=(q,))
    process_reader = Process(target=reader, args=(q,))

    process_wirter.start()
    process_wirter.join()
    process_reader.start()
    process_reader.join()

    print ''
    print '所有数据都写⼊并且读完'
