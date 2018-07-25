# -*- coding: utf-8 -*-

import os
import time
import random
from multiprocessing import Pool


def worker(msg):
    t_start = time.time()
    print("%s开始执⾏,进程号为%d" % (msg, os.getpid()))
    # random.random()随机⽣成0~1之间的浮点数
    time.sleep(random.random() * 2)
    t_stop = time.time()
    print(msg, "执⾏完毕，耗时%0.2f" % (t_stop - t_start))


pool = Pool(3)
for i in range(10):
    pool.apply_async(worker, (i,))

print("----start- ")
pool.close()  # 关闭进程池，关闭后po不再接收新的请求
pool.join()  # 等待po中所有⼦进程执⾏完成，必须放在close语句之后
print("-----end- ")
