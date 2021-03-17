#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/3/15 16:34
# @Author  : handling
# @File    : serialize_tool.py
# @Software: PyCharm

import json
import zlib
from rc4_tool import Rc4_init, rc4_Decrypt, rc4_Encrypt

data_dict = {'RPCFunction': 1,
             'RPCClass': 2,
             'args': ['123', '2222']}

serialize_str = json.dumps(data_dict)  # 序列化
compress_str = zlib.compress(serialize_str)  # 压缩

# 加密
key = 'handling'
msg = compress_str
s = []
Rc4_init(s, key)
rc4_result = rc4_Encrypt(s, msg)  # rc4_result 是最终结果

# 解密
s = []
Rc4_init(s, key)
msg = rc4_Decrypt(s, rc4_result)
compress_str = msg
serialize_str = zlib.decompress(compress_str)  # 解压缩
data_dict = json.loads(serialize_str)  # 反序列化
print data_dict


def rpc_call_data(call_code, args):
    data_dict = {'code' : call_code,
                 'args': list(args)}

    serialize_str = json.dumps(data_dict)  # 序列化
    compress_str = zlib.compress(serialize_str)  # 压缩
    return compress_str


# 强化安全性，使用非对称加密对称加密key值

# 服务器端持有私钥，发送给客户端公钥， 客户端生成RC4Key，并使用公钥加密，发送到服务器端，这样即使RC4key被拦截，也无法被解密
# 而服务器端持有私钥能解密出RC4key，之后就使用RC4key对称加密方式加密即可。
