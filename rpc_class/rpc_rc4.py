#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/3/16 10:39
# @Author  : handling
# @File    : rpc_rc4.py
# @Software: PyCharm

from RPCTools.rpc_code import RPCReturnCode


class RPC_RC4:
    def __init__(self):
        pass

    rc4_key = None

    @staticmethod
    def set_rc4_key(rc4_key):
        RPC_RC4.rc4_key = rc4_key
        return RPCReturnCode.SUCCESS
