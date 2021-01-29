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


def recv_flag(read_sock):
    flag_data = recv_fixed_sz_data(read_sock, 4)
    return bytes_to_int(flag_data)


def send_flag(write_sock, flag):
    flag_data = int_to_bytes(flag)
    send_fixed_sz_data(write_sock, flag_data)


class MessageHandler:

    def __init__(self):
        self.__data = bytearray()
        self.__end_index = 0
        self.__msgs = []
        pass

    def append_new_data(self, data):
        self.__data.extend(data)
        self.__end_index += len(data)

    def decode_message_data(self):
        while True:
            if self.__end_index <= 4:
                break
            msg_len = bytes_to_int(self.__data[0:4])
            if self.__end_index - 4 >= msg_len:
                msg = bytes_to_str(self.__data[4:4+msg_len], msg_len)
                self.__msgs.append(msg)
                self.__data = self.__data[4 + msg_len:]
                self.__end_index -= (4 + msg_len)
            else:
                break
        result_msgs = self.__msgs
        self.__msgs = []
        return result_msgs

    @classmethod
    def encode_msg(cls, msg):
        msg_data = str_to_bytes(msg)
        len_data = int_to_bytes(len(msg_data))
        return len_data + msg_data


class Flag:
    ADD_NEW_CONN_EVENT = 0
    SEND_MSG_TO_CLIENT = 1
    BUFFER_SIZE = 1024

    def __init__(self):
        pass
