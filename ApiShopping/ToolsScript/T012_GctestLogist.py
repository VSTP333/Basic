#!/usr/bin/env python
# encoding: utf-8
'''
@author: wangling
@project: ApiShopping
@file: newlogistdetail.py
@time: 2020-03-09 15:27:01
@desc:
'''

import requests
import json
import random
import time

def logistdetail(type,orderId):
    url = 'http://gctestprexg.admin.cnsuning.com/order/logistics.do'
    headers = {
        'Content-Type': 'application/json'
    }
    code1 = str(int(time.time()))
    code2 = str(random.randint(10000,1000000))
    code3 = str(random.randint(10000,1000000))
    data111 = {
        "orderNo": orderId,
        "orderLogistics":
            [{"packageCode": code1+code2,
              "itemLogistics":
                  [{"orderItemNo": orderId+"01", "num": 2}]}
             ]
    }
    data112 = {
        "orderNo": orderId,
        "orderLogistics":
            [{"packageCode": code1+code2,
              "itemLogistics":
                  [{"orderItemNo": orderId+"01", "num": 1}]},
             {"packageCode": code1 + code3,
              "itemLogistics":
                  [{"orderItemNo": orderId + "01", "num": 1}]}
             ]
    }
    data121 = {
        "orderNo": orderId,
        "orderLogistics":
            [{"packageCode": code1 + code2,
              "itemLogistics":
                  [{"orderItemNo": orderId + "01", "num": 1},
                   {"orderItemNo": orderId + "02", "num": 1}]}
             ]
    }
    data122 = {
        "orderNo": orderId,
        "orderLogistics":
            [{"packageCode": code1 + code2,
              "itemLogistics":
                  [{"orderItemNo": orderId + "01", "num": 1}]},
             {"packageCode": code1 + code3,
              "itemLogistics":
                  [{"orderItemNo": orderId + "02", "num": 1}]}
             ]
    }
    if type==112:
        data =data112
    elif type==121:
        data =data121
    elif type==122:
        data = data122
    else:
        data = data111

    data = json.dumps(data)
    print(data)
    req = requests.post(url=url,data=data,headers=headers)
    print(req.text)

if __name__ =='__main__':
    # type=111 一单一行一包裹100000015104
    # type=112一单一行两包裹100000015105
    # type=121一单两行一包裹100000015106
    # type=122一单两行两包裹100000015107
    logistdetail(type=121,orderId="100000016020")