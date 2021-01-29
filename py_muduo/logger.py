#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 15:41
# @Author  : handling
# @File    : logger.py
# @Software: PyCharm

from threading import current_thread, Lock

logger_lock = Lock()

def simple_log(*args):
    # 可以改动， 增加 writable
    logger_lock.acquire(True)
    print current_thread().name + ':',
    for i in range(len(args)):
        print args[i],
    print ''
    logger_lock.release()
