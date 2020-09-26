#!/usr/bin/env python
# encoding: utf-8
'''
@author: 18056678（郭海龙）
@project: ApiShopping
@file: T015_GctestInvoice.py
@time: 2020-06-18 22:12:45
@desc:
'''
import requests
def Invoice(invoiceId='',status=''):
    url = 'http://gctestprexg.admin.cnsuning.com/invoice/status.do?invoiceId=%s&status=%s' % (invoiceId,status)
    req = requests.get(url)
    print(req.text)


if __name__ == "__main__":
    Invoice(invoiceId='10000018',status='2')