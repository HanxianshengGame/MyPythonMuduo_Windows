# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : sub_reactor_threadpool.py
# @Time     : 2021/1/10 20:55
# @Software : PyCharm
# @Introduce: This is

import logger
from Queue import Queue
from threading import Thread
from event_loop import EventLoop


class SubReactorThread(Thread):
    def __init__(self, name, common_conn_que):
        Thread.__init__(self)
        self.name = name
        self.common_conn_que = common_conn_que
        self.__loop = EventLoop(self.get_new_conn, self.get_conn, self.remove_conn)
        self.__sock_to_conns = {}

    def get_new_conn(self):
        """
        分配到新连接
        :return:
        """
        new_conn = self.common_conn_que.get(1)
        new_conn.set_loop(self.__loop)
        self.__sock_to_conns[new_conn.get_sock()] = new_conn
        self.__loop.register_listen_sock(new_conn.get_sock())
        return new_conn


    def get_conn(self, sock):
        return self.__sock_to_conns[sock]

    def remove_conn(self, sock):
        self.__loop.unregister_listen_sock(sock)
        del self.__sock_to_conns[sock]

    def run(self):
        logger.simple_log('正在运做')
        self.__loop.loop()

    def stop(self):
        self.__loop.un_loop()

    def get_conn_count(self):
        return len(self.__sock_to_conns.keys())


class SubReactorThreadPool:

    def __init__(self, thread_num, ):
        self.__thread_num = thread_num
        self.__reactors = []
        self.__conn_que = Queue(10)
        self.__is_stop = False
        pass

    def start(self):
        self.__is_stop = False
        for i in range(self.__thread_num):
            reactor = SubReactorThread('reactor' + str(i), self.__conn_que)
            self.__reactors.append(reactor)

        for reactor in self.__reactors:
            reactor.start()

    def stop(self):
        if self.__is_stop:
            return
        self.__is_stop = True
        for reactor in self.__reactors:
            reactor.stop()

        for reactor in self.__reactors:
            logger.simple_log('正在关闭 ', reactor.name)
            reactor.join()

    def assign_new_conn(self, conn):
        logger.simple_log('正在分配新连接')
        self.__conn_que.put(conn, True)
        reactor = min(self.__reactors, key=lambda reactor: reactor.get_conn_count())
        logger.simple_log(reactor.name,'分配到了新连接： ', conn.get_peer_addr())
        reactor.get_new_conn()
        pass
