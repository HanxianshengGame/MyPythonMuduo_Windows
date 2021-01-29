#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 11:01
# @Author  : handling
# @File    : client_test.py
# @Software: PyCharm

import socket
import time
import socket_message_handler

client_sock = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)

client_sock.connect(('localhost', 2000))

count = 5
while count:
    socket_message_handler.send_msg_to_client(client_sock, '1111')
    msg = socket_message_handler.recv_msg_from_client(client_sock)
    print '服务器发来了: ', msg
    time.sleep(2)
    count -= 1

client_sock.close()

