# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : type_convert.py
# @Time     : 2021/1/9 10:56
# @Software : PyCharm
# @Introduce: This is

from socket import *
import struct


def int_to_bytes(len):
    format_str = '<i'
    s = struct.Struct(format_str)
    return s.pack(len)


def str_to_bytes(content):
    format_str = '<' + str(len(content)) + 's'
    s = struct.Struct(format_str)
    return s.pack(content)


def bytes_to_int(data):
    format_str = '<i'
    s = struct.Struct(format_str)
    return s.unpack(data)[0]


def bytes_to_str(data, data_len):
    format_str = '<' + str(data_len) + 's'
    s = struct.Struct(format_str)
    return s.unpack(data)[0]


# content = "nihao"
#
# send_data = int_to_bytes(len(content)) + str_to_bytes(content)
# print send_data
#
# data_len = bytes_to_int(send_data[0:4:])
# print data_len

print '----------------'
b = bytearray(b'abcd')

print(b)
b.append(101)
print(b)
b.insert(0, 65)
print(b)
b.extend('111111')
print(b)
b.pop(0)
print(b)
b.remove(101)
print(b)


class Message:
    def __init__(self):
        self.data = bytearray()
        self.end_index = 0
        self.msgs = []
        pass

    def append_new_data(self, data):
        self.data.extend(data)
        self.end_index += len(data)

    def read_message(self):
        while True:
            if self.end_index <= 4:
                break
            msg_len = bytes_to_int(self.data[0:4])
            if self.end_index - 4 >= msg_len:
                msg = bytes_to_str(self.data[4:], msg_len)
                self.msgs.append(msg)
                self.data = self.data[4 + msg_len:]
                self.end_index -= 4 + msg_len
            else:
                break
        result_msgs = self.msgs
        self.msgs = []
        return result_msgs



msg = Message()

data_bytes = str_to_bytes('1111')
data_len_bytes = int_to_bytes(len(data_bytes))


msg.append_new_data(data_len_bytes + data_bytes)
msgs = msg.read_message()
print msgs
data_bytes = str_to_bytes('1111')
data_len_bytes = int_to_bytes(len(data_bytes))


msg.append_new_data(data_len_bytes + data_bytes)
msgs = msg.read_message()
print msgs
data_bytes = str_to_bytes('1111')
data_len_bytes = int_to_bytes(len(data_bytes))


msg.append_new_data(data_len_bytes + data_bytes)
msgs = msg.read_message()
print msgs
