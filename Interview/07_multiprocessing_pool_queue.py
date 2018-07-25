# -*- coding: utf-8 -*-

import os
from multiprocessing import Pool, Manager


def wirter(q):
    print("writer启动(%s),⽗进程为(%s)" % (os.getpid(), os.getppid()))
    for i in "dongGe":
        q.put(i)


def reader(q):
    print("reader启动(%s),⽗进程为(%s)" % (os.getpid(), os.getppid()))
    for i in range(q.qsize()):
        print("reader从Queue获取到消息：%s" % q.get(True))


if __name__ == "__main__":
    print("(%s) start" % os.getpid())
    q = Manager.Queue()
    pool = Pool()
    pool.apply(wirter, (q, ))
    pool.apply(reader, (q, ))

    pool.close()
    pool.join()
    print("(%s) End" % os.getpid())
