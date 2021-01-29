# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : acceptor.py
# @Time     : 2021/1/10 19:11
# @Software : PyCharm
# @Introduce: This is

import socket
class Acceptor:

    def __init__(self, ip, port):
        self.__addr = (ip, port)
        self.__listen_sock = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)
        pass

    def __set_reuse_addr(self):
        self.__listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def __bind(self):
        self.__listen_sock.bind(self.__addr)

    def __listen(self):
        self.__listen_sock.listen(10)

    def ready(self):
        self.__set_reuse_addr()
        self.__bind()
        self.__listen()
        self.__listen_sock.setblocking(False)
        pass

    def get_listen_fd(self):
        return self.__listen_sock.fileno()

    def get_listen_sock(self):
        return self.__listen_sock


    def accept(self):
        client_sock, client_addr = self.__listen_sock.accept()
        return client_sock, client_addr


