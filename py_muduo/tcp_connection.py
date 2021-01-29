# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : tcp_connection.py
# @Time     : 2021/1/10 19:26
# @Software : PyCharm
# @Introduce: This is
from socket_message_handler import send_fixed_sz_data, MessageHandler


class TcpConnection:
    on_connection_callback = None
    on_message_callback = None
    on_close_callback = None

    def __init__(self, client_sock):
        self.__sock = client_sock
        self.__event_loop = None
        """
        IO socket 搭配epoll 一般是非阻塞+边缘触发ET
        """
        self.__sock.setblocking(False)
        self.__local_addr = client_sock.getsockname()
        self.__peer_addr = client_sock.getpeername()
        self.__msg_handler = MessageHandler()

        pass

    def set_loop(self, event_loop):
        self.__event_loop = event_loop

    def recv_msg(self):
        while True:
            # 1. recv 如果本次接收时缓冲区无数据抛出异常，（errorno == 11）
            # 2. recv 如果本次接收时对端关闭返回None
            # 3. recv 如果接收的消息不足以解析，或者这边缓冲区仅有 4（11）+ 10，
            data = self.__sock.recv(1024)
            if not data:
                break
            self.__msg_handler.append_new_data(data)
            msgs = self.__msg_handler.decode_message_data()
            if len(msgs):
                return msgs, False
        return [], True

    def send_msg(self, msg):
        data = self.__msg_handler.encode_msg(msg)
        send_fixed_sz_data(self.__sock, data)
        pass

    def send_in_loop(self, msg):
        if self.__event_loop:
            self.__event_loop.run_in_loop(self.__sock,self.send_msg, msg)

    def close(self):
        self.__sock.close()

    def get_peer_addr(self):
        return self.__peer_addr

    def get_fd(self):
        return self.__sock.fileno()


    def get_sock(self):
        return self.__sock

    def handle_message_callback(self):
        return TcpConnection.on_message_callback(self)

    def handle_connection_callback(self):
        TcpConnection.on_connection_callback(self)

    def handle_close_callback(self):
        TcpConnection.on_close_callback(self)
