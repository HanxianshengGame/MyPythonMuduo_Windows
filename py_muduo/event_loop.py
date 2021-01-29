#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:01
# @Author  : handling
# @File    : event_loop.py
# @Software: PyCharm
import select
import errno
import socket
from threading import Lock


class EventLoop:

    def __init__(self, get_new_conn_func, get_conn_func,
                 remove_conn_func):

        self.__get_new_conn_func = get_new_conn_func
        self.__get_conn_func = get_conn_func
        self.__remove_conn_func = remove_conn_func

        self.__lock = Lock()
        self.__send_funcs = []  # 存放了自身所管理的连接的未处理的发送事件

        self.__is_looping = False

        self.inputs = []
        self.outputs = []

    def register_listen_sock(self, sock):
        self.inputs.append(sock)

    def unregister_listen_sock(self, sock):
        self.inputs.remove(sock)

    def __handle_conn_close(self, sock):
        self.__get_conn_func(sock).close()
        self.__remove_conn_func(sock)

    def run_in_loop(self, sock, send_func, msg):
        self.__lock.acquire(True)
        self.outputs.append(sock)
        self.__send_funcs.append((send_func, msg))
        self.__lock.release()

    def do_send_funcs(self):
        self.__lock.acquire(True)
        tmp = self.__send_funcs
        self.__send_funcs = []
        self.outputs = []
        self.__lock.release()
        for send_func, msg in tmp:
            send_func(msg)


    def un_loop(self):
        if self.__is_looping:
            self.__is_looping = False


    def loop(self):
        # 监听read_sock 并执行 添加新连接的事件
        self.__is_looping = True
        while self.__is_looping:
            if len(self.inputs):
                readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0.1)
                if not (readable or writable or exceptional):
                    # logger.simple_log('暂时没有客户端进行通信')
                    continue

                # 有消息发送
                if len(writable):
                    self.do_send_funcs()

                for sock in readable:
                    conn = self.__get_conn_func(sock)
                    try:
                        while True:
                            need_close = conn.handle_message_callback()
                            if need_close:
                                conn.handle_close_callback()
                                self.__handle_conn_close(sock)
                                break

                    except socket.error as error_msg:
                        if error_msg.errno != errno.EWOULDBLOCK:
                            print error_msg.errno
                            conn.handle_close_callback()
                            self.__handle_conn_close(sock)

                for sock in exceptional:
                    conn = self.__get_conn_func(sock)
                    conn.handle_close_callback()
                    self.__handle_conn_close(sock)
