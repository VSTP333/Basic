#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: url_code.py
@time: 2019-12-17 11:15:43
@desc:
'''

from urllib.parse import quote,unquote

def urlencode(text):
    #url编码
    u = quote(text,'utf-8')
    return u

def urldecode(text):
    #url解码
    u = unquote(text,'utf-8')
    return u
