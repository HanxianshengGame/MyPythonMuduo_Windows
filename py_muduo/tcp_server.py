# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : tcp_server.py
# @Time     : 2021/1/10 19:44
# @Software : PyCharm
# @Introduce: This is

import logger
from acceptor import Acceptor
from acceptor_loop import AcceptorLoop
from sub_reactor_threadpool import SubReactorThreadPool


class TcpServer:
    def __init__(self, ip, port, sub_reactor_num):
        self.__acceptor = Acceptor(ip, port)
        self.__loop = AcceptorLoop(self.__acceptor)
        self.__sub_reactors = SubReactorThreadPool(sub_reactor_num)
        pass

    def start(self):
        self.__sub_reactors.start()
        self.__acceptor.ready()
        self.__loop.loop(self.__sub_reactors)
        self.close()
        pass

    def close(self):
        logger.simple_log('正在停止新连接的接收')
        self.__loop.un_loop()
        logger.simple_log('正在关闭 reactors')
        self.__sub_reactors.stop()
        pass
