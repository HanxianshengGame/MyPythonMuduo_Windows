#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/3/16 10:25
# @Author  : handling
# @File    : rpc_code.py
# @Software: PyCharm


class RPCCallCode(object):
    SET_RC4_KEY = 0
    LOGIN = 1
    REGISTER = 2
    START_GAME = 100
    pass


class RPCReturnCode(object):
    FAILURE = 0
    SUCCESS = 1
    pass
