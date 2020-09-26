#!/usr/bin/env python
# encoding: utf-8
'''
@author: 18056678（郭海龙）
@project: ApiShopping
@file: T014_GctestBill.py
@time: 2020-06-18 22:03:21
@desc:
'''
import requests
def Bill(custNo='',startTime='',endTime=''):
    url = 'http://gctestprexg.admin.cnsuning.com/bill/create.do?custNo=%s&start=%s&end=%s' %(custNo,startTime,endTime)
    req = requests.get(url)
    print(url)
    print(req.text)

if __name__ == '__main__':
    Bill(custNo='7030088163',startTime='2020-06-01',endTime='2020-06-19')