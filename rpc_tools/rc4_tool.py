#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/3/15 17:39
# @Author  : handling
# @File    : rc4_tool.py
# @Software: PyCharm

import hashlib
import base64


def Rc4_init(S, K):  # S盒初始化置换,K为密钥
    j = 0
    K = hashlib.md5(K).hexdigest()
    k = []  # 临时数组
    for i in range(256):
        S.append(i)
        k.append(K[i % len(K)])
    for i in range(256):
        j = (j + S[i] + ord(k[i])) % 256
        S[i], S[j] = S[j], S[i]  # 交换S[i],S[j]


def rc4_Encrypt(S, D):
    i = j = 0
    result = ''
    for a in D:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256

        k = chr(ord(a) ^ S[(S[i] + S[j]) % 256])
        result += k
    result = base64.b64encode(result)
    return result


def rc4_Decrypt(S, D):
    i = j = 0
    D = base64.b64decode(D)
    result = ''
    for a in D:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256

        k = chr(ord(a) ^ S[(S[i] + S[j]) % 256])
        result += k
    return result
#
#
# key = 'dasdffdghfghjde'
# d = 'thisisatest'
# print("key:"+key)
# print("m:"+d)
#
#
# s=[]
# Rc4_init(s, key)
# print("s盒:")
# print(s)
#
# c = rc4_Encrypt(s, d)
# print("Encrypt:"+c)
#
#
# s=[]
# Rc4_init(s,key)
# print("s盒:")
# print(s)
# z = rc4_Decrypt(s, c)
# print("Decrypt:"+z)