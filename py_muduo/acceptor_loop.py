#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:00
# @Author  : handling
# @File    : acceptor_loop.py
# @Software: PyCharm

import select
import logger
from tcp_connection import TcpConnection


class AcceptorLoop:

    def __init__(self, acceptor):
        self.__acceptor = acceptor
        self.inputs = [self.__acceptor.get_listen_sock()]
        self.outputs = []
        self.__is_looping = False
        pass

    def un_loop(self):
        if self.__is_looping:
            self.__is_looping = False

    def loop(self, sub_reactors):
        self.__is_looping = True
        logger.simple_log('正在接受玩家连接')
        while self.__is_looping:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs,10)
            if len(readable) == 0:
                logger.simple_log('暂时没有新玩家连接')
                continue

            for s in readable:
                client_sock, client_addr = self.__acceptor.accept()
                new_conn = TcpConnection(client_sock)
                new_conn.handle_connection_callback()
                sub_reactors.assign_new_conn(new_conn)

            for s in exceptional:
                logger.simple_log('服务端接收客户端出现错误, 紧急关闭')
                self.inputs.remove(self.__acceptor.get_listen_sock())
                break
        pass
