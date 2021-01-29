#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 16:26
# @Author  : handling
# @File    : main.py
# @Software: PyCharm
import logger
import signal
from task import Task
from tcp_server import TcpServer
from compute_threadpool import ComputeThreadPool
from tcp_connection import TcpConnection


class GameServer:

    def __init__(self, ip, port, reactor_num=5):
        self.__compute_thread_pool = compute_thread_pool
        self.__server = TcpServer(ip, port, reactor_num)

    def start(self):
        TcpConnection.on_connection_callback = on_connection
        TcpConnection.on_message_callback = on_message
        TcpConnection.on_close_callback = on_close
        self.__compute_thread_pool.start()
        self.__server.start()

    def close(self):
        self.__server.close()
        logger.simple_log('正在关闭计算线程池')
        self.__compute_thread_pool.stop()
        pass


def on_connection(conn):
    logger.simple_log('新的玩家连接：', conn.get_peer_addr())
    pass


def on_message(conn):
    msgs, need_close = conn.recv_msg()
    for msg in msgs:
        logger.simple_log(conn.get_peer_addr(), "发来了消息：", msg)
        compute_thread_pool.add_task(Task(conn, msg))
    return need_close


def on_close(conn):
    logger.simple_log(conn.get_peer_addr(), ' close!')


def handler(signum, frame):
    print 'Signal handler called with signal', signum
    print '服务器正在终止中'
    game_server.close()


signal.signal(signal.SIGINT, handler)
compute_thread_pool = ComputeThreadPool(5, 20)
game_server = GameServer('localhost', 2000, 5)
game_server.start()
