# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : socket_test.py
# @Time     : 2021/1/9 14:45
# @Software : PyCharm
# @Introduce: This is
import select
import Queue
import struct
import socket


def int_to_bytes(convert_val):
    format_str = '<i'
    s = struct.Struct(format_str)
    return s.pack(convert_val)


def str_to_bytes(convert_val):
    format_str = '<' + str(len(convert_val)) + 's'
    s = struct.Struct(format_str)
    return s.pack(convert_val)


def bytes_to_int(convert_data):
    format_str = '<i'
    s = struct.Struct(format_str)
    return s.unpack(convert_data)[0]


def bytes_to_str(convert_data, data_len):
    format_str = '<' + str(data_len) + 's'
    s = struct.Struct(format_str)
    return s.unpack(convert_data)[0]


def recv_fixed_sz_data(sock, recv_sz):
    total = 0
    result_data = ''
    while total < recv_sz:
        data = sock.recv(recv_sz - total)
        if data:
            result_data += data
            total += len(data)
        else:
            return int_to_bytes(0)
    return result_data


def recv_client_msg(sock):
    data_len = bytes_to_int(recv_fixed_sz_data(sock, 4))
    if not data_len:
        return None
    msg = bytes_to_str(recv_fixed_sz_data(sock, data_len), data_len)
    if not msg:
        return None
    return msg


server_sock = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_addr = ('localhost', 2000)
server_sock.bind(server_addr)
server_sock.listen(10)

print '服务器启动成功， 监听IP：', server_addr

server_sock.setblocking(True)

timeout = 10
message_queues = {}
fd_to_socket = {server_sock.fileno(): server_sock}
buffer_sz = 1024


inputs = [server_sock]
outputs = []

while inputs:
    print '正在接受玩家连接'
    readable, writable, exceptional = select.select(inputs, outputs, inputs,10)
    for s in readable:
        if s is server_sock:
            client_sock, client_addr = s.accept()
            print ' connection from', client_addr
            client_sock.setblocking(0)
            inputs.append(client_sock)
            message_queues[client_sock] = Queue.Queue()
        else:
            data = s.recv(buffer_sz)
            if data:
                print 'received {0} from {1}'.format(data, s.getpeername())
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print 'closing',  s.getpeername()
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            print ' ', s.getpeername(), 'queue empty'
            outputs.remove(s)
        else:
            print 'sending {0} to {1}'.format(next_msg, s.getpeername())
            s.send(next_msg)

    for s in exceptional:
        print 'exception condition on', s.getpeername()
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        del message_queues[s]



