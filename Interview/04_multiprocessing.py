# -*- coding: utf-8 -*-
import os
from multiprocessing import Process


def run_proc(name):
    print('⼦进程运⾏中，name= %s ,pid=%d...' % (name, os.getpid()))


if __name__ == "__main__":
    process = Process(target=run_proc, args=('test',))
    print('⼦进程将要执⾏')
    process.start()
    # print('⼦进程将要join')
    # process.join()
    print('⼦进程已结束')
