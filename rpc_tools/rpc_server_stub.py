#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/3/16 11:11
# @Author  : handling
# @File    : rpc_server_stub.py
# @Software: PyCharm

from rpc_class.rpc_rc4 import RPC_RC4
from rpc_code import RPCCallCode


class RPCServerStub(object):
    code_to_func = {RPCCallCode.SET_RC4_KEY: RPC_RC4.set_rc4_key}

    def __init__(self):
        pass

    @classmethod
    def get_func(cls, func_code):
        return cls.code_to_func[func_code]