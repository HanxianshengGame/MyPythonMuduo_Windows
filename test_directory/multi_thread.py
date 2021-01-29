# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : multi_thread.py
# @Time     : 2021/1/10 16:13
# @Software : PyCharm
# @Introduce: This is

import threading
import time
from random import randint
from time import sleep
from Queue import Queue

exit_flag = 0


def print_time(thread_name, delay, counter):
    while counter:
        if exit_flag:
            thread_name.exit()
        time.sleep(delay)
        print ("%s: %s " % (thread_name, time.ctime(time.time())))
        counter -= 1


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print '开始线程：' + self.name
        thread_lock.acquire()
        print_time(self.name, 5, self.counter)
        print '退出线程: ' + self.name
        thread_lock.release()


thread_lock = threading.Lock()

#
# thread1 = MyThread(1, "Thread-1", 1)
# thread2 = MyThread(2, "Thread-2", 2)
#
# thread1.start()
# thread2.start()
#
# thread1.join()
# thread2.join()


class MyThread2(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

    pass

def func1():
    print threading.current_thread(), 'running'
    pass

t1 = MyThread2(func1, (), '1')
t2 = MyThread2(func1, (), '2')

t1.start()
t2.start()

t1.join()
t2.join()




def write_queue(queue):
    print 'product object for q.....'
    queue.put('xxx', 1)
    print 'size now', queue.qsize()


def read_queue(queue):
    val = queue.get(1)
    print 'consumed object from q.... size now', \
        queue.qsize()


def writer(queue, loops):
    for i in range(loops):
        write_queue(queue)
        sleep(randint(1, 3))


def reader(queue, loops):
    for i in range(loops):
        read_queue(queue)
        sleep(randint(2, 5))


funcs = [writer, reader]
nfuncs = range(len(funcs))


def main():
    nloops = randint(2, 5)
    q = Queue(32)
    threads = []
    for i in nfuncs:
        t = MyThread2(funcs[i], (q, nloops),funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
       threads[i].start()
       pass

    for i in nfuncs:
        threads[i].join()

    print 'all done'

if __name__ == '__main__':
    main()
