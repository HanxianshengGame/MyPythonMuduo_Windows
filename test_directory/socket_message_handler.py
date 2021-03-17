#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 14:19
# @Author  : handling
# @File    : socket_message_handler.py
# @Software: PyCharm


import struct
import json


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


class JsonDataResponseEntity:
    def __init__(self, actionCode, data):
        self.actionCode = actionCode
        self.data = data
        pass


class JsonDataRequestEntity:
    def __init__(self, requestCode, actionCode, data):
        self.requestCode = requestCode
        self.actionCode = actionCode
        self.data = data
        pass

def handle(dict_obj):
    return JsonDataRequestEntity(dict_obj['requestCode'],
        dict_obj['actionCode'],
        dict_obj['data'])

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

                json_str = bytes_to_str(self.__data[4: 4 + msg_len], msg_len)
                print 'json_data_request_entity: ', json_str
                json_data_request_entity = json.loads(json_str, object_hook=handle)
                request_code = json_data_request_entity.requestCode
                action_code = json_data_request_entity.actionCode
                data = json_data_request_entity.data
                # request_code = bytes_to_int(self.__data[4:8])
                # action_code = bytes_to_int(self.__data[8:12])
                # data_len = msg_len - 8
                # data = bytes_to_str(self.__data[12: 12 + data_len], data_len)
                # task 处理的 msg格式 (request_code, action_code, data)
                self.__msgs.append((request_code, action_code, data))
                self.__data = self.__data[4 + msg_len:]
                self.__end_index -= (4 + msg_len)
            else:
                break
        result_msgs = self.__msgs
        self.__msgs = []
        return result_msgs

    @classmethod
    def encode_msg_data(cls, msg):
        action_code = msg[0]
        data = msg[1]
        json_data_response_entity = JsonDataResponseEntity(action_code, data)
        json_str = json.dumps(json_data_response_entity, default=lambda obj: obj.__dict__,
            sort_keys=True)
        # action_code_bytes = int_to_bytes(action_code)
        # data_bytes = str_to_bytes(data)
        print 'json_data_response_entity: ', json_str
        data_bytes = str_to_bytes(json_str)
        len_bytes = int_to_bytes(len(data_bytes))
        return len_bytes + data_bytes


class Flag:
    ADD_NEW_CONN_EVENT = 0
    SEND_MSG_TO_CLIENT = 1
    BUFFER_SIZE = 1024

    def __init__(self):
        pass
