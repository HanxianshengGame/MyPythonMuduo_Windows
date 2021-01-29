#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 14:19
# @Author  : handling
# @File    : socket_message_handler.py
# @Software: PyCharm


import struct


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
            return None
    return result_data


def send_fixed_sz_data(sock, data):
    send_len = 0
    while send_len != len(data):
        send_len += sock.send(data[send_len:])
    pass


# decode 解包
def recv_msg_from_client(sock):
    """
    TODO 涉及拆包的逻辑
    :param sock:
    :return:
    """
    len_data = recv_fixed_sz_data(sock, 4)
    if not len_data:
        return None
    data_len = bytes_to_int(len_data)

    msg_data = recv_fixed_sz_data(sock, data_len)
    if not msg_data:
        return None
    msg = bytes_to_str(msg_data, data_len)
    return msg


# encode 装包
def send_msg_to_client(sock, msg):
    """
    涉及装包的逻辑
    :param sock:
    :param msg:
    :return:
    """
    msg_data = str_to_bytes(msg)
    len_data = int_to_bytes(len(msg_data))
    send_fixed_sz_data(sock, len_data + msg_data)
    pass


def recv_flag(read_sock):
    flag_data = recv_fixed_sz_data(read_sock, 4)
    return bytes_to_int(flag_data)


def send_flag(write_sock, flag):
    flag_data = int_to_bytes(flag)
    send_fixed_sz_data(write_sock, flag_data)


class Flag:
    ADD_NEW_CONN_EVENT = 0
    SEND_MSG_TO_CLIENT = 1

    def __init__(self):
        pass
