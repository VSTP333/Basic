#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: base64_en.py
@time: 2019-12-17 11:10:57
@desc:
'''

import base64

def ba64encode(text):
    bs = base64.b64encode(str(text).encode("utf-8")) # 将字符为unicode编码转换为utf-8编码
    return bs  # 得到的编码结果前带有 b

def ba64decode(text):
    bs = str(base64.b64decode(str(text)), "utf-8")
    return bs  # 解码

def ba64encode_u(text):
    bs = str(base64.b64encode(str(text).encode("utf-8")), "utf-8")
    return bs # 去掉编码结果前的 b

def ba64decode_u(text):
    bs = str(base64.b64decode(str(text)), "utf-8")
    return bs  # 解码

if __name__ == '__main__':
    dd=ba64encode(text='sdasd')
    print(dd)
