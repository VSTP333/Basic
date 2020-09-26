#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: md5.py
@time: 2019-05-09 11:40:49
@desc:对字符串进行MD5加密
'''

import hashlib

class Md5(object):
    "生成MD5加密的密文"
    def __init(self,text):
        text = str(text)
        tmp_text = hashlib.md5()
        tmp_text.update(text.encode(encoding="utf-8"))
        text_md5 = tmp_text.hexdigest()
        return text_md5

    def getMd5_16(self,text=None,upper=False):
        text_md5 = self.__init(text)
        "返回16位MD5加密的密文"
        if upper:
            text_md5 = text_md5.upper()
        return text_md5[8:24]

    def getMd5_32(self,text=None,upper=False):
        text_md5 = self.__init(text)
        "返回32位MD5加密的密文"
        if upper:
            text_md5 = text_md5.upper()
        return text_md5