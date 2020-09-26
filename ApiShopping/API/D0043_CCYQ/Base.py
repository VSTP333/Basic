#!/usr/bin/env python
# encoding: utf-8
'''
@author: 18056678（郭海龙）
@project: ApiShopping
@file: Base.py
@time: 2019-12-24 17:44:06
@desc:
'''
import json
import time

from API.D0043_CCYQ.url import Link
from Tools.AES_cryption import Aes_ECB
from Tools.base64_en import ba64encode_u
from Tools.tools import Common
from Tools.tools import MySql, Md5
from Tools.url_code import urlencode


class API():
    def __init__(self,envi,user,isLog):
        self.mysql=MySql(envi)
        self.common = Common(envi=envi)

        self.appkey = user
        self.appSecret =self.common.getSecret(appKey=user)
        # self.appSecret ='09055208-2aed-4618-8e9e-ab51bdca203d'

        self.host = self.common.scHost()
        self.nowtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        self.now = time.time()
        self.isLog = isLog
        text = str(self.appkey) + '|' + str(self.appSecret) + '|' + str(int((self.now * 1000)) + 10 * 60 * 1000)

        key = Md5().getMd5_32(self.appSecret)[0:16]

        accessToken = Aes_ECB(key).AES_encrypt(text)  # AES加密
        accessToken = urlencode(accessToken)  # url编码
        accessToken = ba64encode_u(accessToken)  # base64编码

        self.headers = {
            "Content-Type": "application/json",
            "accessToken": accessToken,
            "clientId": self.appkey,
            "time": str(int(self.now) * 1000),
            "traceId": "123"
        }
        # print(self.headers)

    def handMsg(self,event='',pcode='',status=None,business='',level=None,billStatus=None,pBillCode='',code='',name='',parentCode='',lowCode='',newCode='',reason='',itemCode='',itemPcode=''):
        FuncName = self.handMsg.__doc__
        url = Link.HandMsg.url
        # 订单类
        if business == 'ORDER':
            # 新增订单
            if event == 'ADD':
                data = {
                     "business": "ORDER",
                     "event": event,
                     "time": int(self.now) * 1000,
                     "msgId": str(int(self.now)),
                     "data": {"pcode": pcode}
                }
            # 确认或取消订单
            elif event == 'CONFIRM':
                data = {
                    "business": "ORDER",
                    "event": event,
                    "time": int(self.now) * 1000,
                    "msgId": str(int(self.now)),
                    "data": {"pcode": pcode,"status":status}
                }
            # 取消订单
            elif event == 'CANCEL':
                data = {
                    "business":"ORDER",
                    "event":event,
                    "msgId":str(int(self.now)),
                    "data":{"code":code}
                }
        # 同步类目，只存储显示
        elif business == "GOODS_CATEGORY":
            data = {
                "business":"GOODS_CATEGORY",
                "event":"SYNC",
                "msgId":str(int(self.now)),
                "data":{"code":code,"level":level,"name":name,"parentCode":parentCode,"status":status}
            }
        # 同步地址库，只存储显示
        elif business == "AREA":
            data = {
                "business":"AREA",
                "event":"SYNC",
                "msgId":str(int(self.now)),
                "data":{"lowCode":lowCode,"newCode":newCode,"parentCode":parentCode,"name":name,"level":level,"status":status}
            }
        # 订单收货和退货
        elif business == "RECEIVE" or business == "REFUND":
            data = {
                "business":business,
                "event":"ADD",
                "time":int(self.now) * 1000,
                "msgId":str(int(self.now)),
                "data":{"pcode":pcode}
            }
        # 账单
        elif business == "BILL":
            # 接收对账单确认/驳回
            if event == "CONFIRM":
                data = {
                    "business":"BILL",
                    "event":event,
                    "msgId":str(int(self.now)),
                    "traceId":str(int(self.now)),
                    "data":{"code":code,"pcode":pcode,"reason":reason,"status":status}
                }
            # 对账单结果消息
            elif event == "RESULT":
                items = []
                for item in itemCode.split(','):
                    items.append({"itemCode":item,"status":status,"billStatus":billStatus,"pBillCode":pBillCode})
                data = {
                    "business":"BILL",
                    "event":event,
                    "msgId":str(int(self.now)),
                    "data":{"code":code,"items":items}
                }
        # 发票
        elif business == "INVOICE":
            if event == 'ADD':
                data = {
                    "business":"INVOICE",
                    "event":"ADD",
                    "msgId":str(int(self.now)),
                    "data":{"pcode":pcode}
                }
            else:
                data = {
                    "business": "INVOICE",
                    "event": "CONFIRM",
                    "msgId": str(int(self.now)),
                    "data": {"pcode": pcode,"status":status}
                }
        elif business == "ORDER_ITEM":
            items = []
            i = 0
            itemPcode = itemPcode.split(",")
            for item in itemCode.split(","):
                items.append({"itemCode": item, "itemPcode": itemPcode[i]})
                i += 1
            data = {
                "business": "ORDER_ITEM",
                "event": event,
                "msgId": str(int(self.now)),
                "data": {"code": code, "pcode": pcode, "items": items}
            }

        print("消息接口入参：", json.dumps(obj=data, ensure_ascii=False))
        redata = self.common.post(FuncName=FuncName,url =self.host+url, headers=self.headers,data=data,isJson='Y',isLog=self.isLog)
        print("消息接口出参：", json.dumps(obj=redata, ensure_ascii=False))
        return redata

    def getProdPriceAndTaxcode(self, skus='',provinceCode='320000000000',citycode='320100000000',countyCode='320102000000',townCode='320102010000'):
            """
            获取价格及税率
            :param sku: 支持批量，最多100
            :return:
            """
            FuncName = self.getProdPriceAndTaxcode.__doc__
            url = Link.GetPriceAndTaxcode.url
            data=[]
            for sku in skus.split(","):
                data.append({"skuId":sku,"count":2,"area":{"provinceCode":provinceCode,"cityCode":citycode, "countyCode":countyCode,"townCode":townCode}})
            # print(self.headers)
            print("获取商品价格及税率接口入参：", json.dumps(obj=data, ensure_ascii=False))
            redata = self.common.post(url=self.host + url, data=data, headers=self.headers,FuncName=FuncName, isJson='Y',isLog=self.isLog)
            print("获取商品价格及税率接口出参：", json.dumps(obj=redata, ensure_ascii=False))
            return redata

    def checkSalearea(self, skus='',provinceCode='320000000000',citycode='320100000000',countyCode='320102000000',townCode='320102010000'):
            """
            校验商品售卖区域
            :param sku: 支持批量，最多100
            :return:
            """
            FuncName = self.checkSalearea.__doc__
            url = Link.CheckSaleStatus.url
            data=[]
            for sku in skus.split(","):
                data.append({"skuId":sku,"area":{"provinceCode":provinceCode,"cityCode":citycode, "countyCode":countyCode,"townCode":townCode}})

            print("校验商品售卖区域接口入参：", json.dumps(obj=data, ensure_ascii=False))
            redata = self.common.post(url=self.host + url, data=data, headers=self.headers, FuncName=FuncName,isJson='Y', isLog=self.isLog)
            print("校验商品售卖区域接口出参：", json.dumps(obj=redata, ensure_ascii=False))
            return redata
    def getShelvesStatus(self, skus=''):
            """
            获取商品上下架状态
            :param sku: 支持批量，最多100
            :return:
            """
            FuncName = self.getShelvesStatus.__doc__
            url = Link.GetShelvesStatus.url
            data=[]
            for sku in skus.split(","):
                data.append({"skuId":sku})

            print("获取商品上下架状态接口入参：", json.dumps(obj=data, ensure_ascii=False))
            redata = self.common.post(url=self.host + url, data=data, headers=self.headers, FuncName=FuncName,isJson='Y', isLog=self.isLog)
            print("获取商品上下架状态接口出参：", json.dumps(obj=redata, ensure_ascii=False))
            return redata

    def getStockStatus(self, skus='',nums='2', provinceCode='110000000000',citycode='110100000000',countyCode='110101000000',townCode='110101001000'):
            """
            校验商品是否有库存
            :param sku: 支持批量，最多100
            :return:
            """
            FuncName = self.getStockStatus.__doc__
            url = Link.CheckStockStatus.url
            data = []
            skulist=skus.split(",")
            numslist=nums.split(",")
            i=0
            for sku in skulist:
                if len(numslist)==1:
                    data.append({"skuId":sku,"count":numslist[0],"area":{"provinceCode":provinceCode,"cityCode":citycode, "countyCode":countyCode,"townCode":townCode}})
                elif len(numslist)==len(skulist):
                    data.append({"skuId": sku, "count":numslist[i],"area": {"provinceCode": provinceCode, "cityCode": citycode, "countyCode": countyCode,"townCode": townCode}})
                    i=i+1
                else:
                    print("商品编码数量与商品个数数量不一致")
                    return
            print("获取商品库存状态接口入参：", json.dumps(obj=data, ensure_ascii=False))
            redata = self.common.post(url=self.host + url, data=data, headers=self.headers, FuncName=FuncName,isJson='Y', isLog=self.isLog)
            print("获取商品库存状态接口出参：", json.dumps(obj=redata, ensure_ascii=False))
            return redata
    def getLogistic(self,code=''):
        """获取物流"""
        FuncName = self.getLogistic.__doc__
        url = Link.GetLogisticsDetail.url
        data = {
            "logisticsOrderCode":code
        }
        print("获取订单物流接口入参：", json.dumps(obj=data, ensure_ascii=False))
        redata = self.common.post(url=self.host + url, data=data, headers=self.headers, FuncName=FuncName, isJson='Y',
                                  isLog=self.isLog)
        print("获取订单物流接口出参：", json.dumps(obj=redata, ensure_ascii=False))
        return redata

