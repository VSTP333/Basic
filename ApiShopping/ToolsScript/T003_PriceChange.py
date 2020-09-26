#!/usr/bin/env python
# encoding: utf-8
'''
@author: zhangqifu
@project: ApiShopping
@file: T003_PriceChange.py
@time: 2019-10-23 16:51:15
@desc: 模拟kafka下发价格变动
'''

from kafka import KafkaProducer
import json,time,random

def PriceChange(cmmdtyCode,cityCode):
    producer = KafkaProducer(bootstrap_servers='10.200.186.79:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    versionNo = int(time.time())
    price = (random.randint(10, 100000)) / 100
    producer.send("PCMS_RESULT",
                    [{"srcSystem": "sync", "dataType": "", "cmmdtyCode": cmmdtyCode.zfill(18), "supplierCode": "",
                      "locatCode": "", "plantCode": "", "cityCode": cityCode, "subCode": "", "zCode": "",
                      "chan": "1",
                      "inventoryFlag": "1",
                      "upState": "",
                      "sourceFlag": "1",
                      "snPrice":price,
                      "refPrice": price, "mpsPrice": price, "mpsPriceType": "",
                      "governmentPrice": price,
                      "maPrice": "", "price": "0", "currency": "", "priceType": "", "startTime": "",
                      "endTime": "", "optFlag": "A", "tranId": "", "tranCount": "",
                      "versionNo": str(versionNo),
                      "versionTime": "", "createTime": "", "updateTime": "",
                      "proPrice": price,
                      "bizCode": "0000000000", "bizType": "", "isPriceDelFlag": ""}])
    producer.close()

if __name__ == '__main__':
    cmmdtyCode = '121347740'

    cityCode='000001000173'
    #北京 000001000000
    #南京 000001000173

    PriceChange(cmmdtyCode,cityCode)

