#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:03
# @Author  : handling
# @File    : task.py
# @Software: PyCharm


class Task:
    def __init__(self, conn, msg):
        self.__conn = conn
        self.__msg = msg

    def process(self):
        """
        该函数会交付给线程池处理
        :return:
        """
        # compute
        # 拿到最终结果
        response = self.__msg
        # 发送
        self.__conn.send_in_loop(response)
