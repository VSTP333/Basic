#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: T007_AutarkyReturn.py
@time: 2019-10-23 16:48:17
@desc: 自营退货脚本
'''

import requests
import json,time
import random
import datetime
from dateutil.relativedelta import relativedelta

class FuncBase():
    def __init__(self,warehouseCode='L025',logisticOrderId=''):
        self.warehouseCode=warehouseCode
        self.logisticOrderId=logisticOrderId
        self.session=requests.session()
        Request_URL = 'https://uiapre.cnsuning.com/ids/login'
        self.headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        login_data = {
            "service": "http://jwmspre.cnsuning.com/jwms-web/auth?targetUrl=http%3A%2F%2Fjwmspre.cnsuning.com%2Fjwms-web%2Findex.html",
            "uuid": "bd8022a3-dfff-42b8-89d9-d1e33c0f1595",
            "loginTheme": "portal",
            "username": "18063468",
            "password": "18063468",
        }
        self.login_result = self.session.post(Request_URL, data=login_data, headers=self.headers)


    def queryVess(self):
        ##获取容器编码
        url='http://jwmsadminpre.cnsuning.com/jwms-admin/base/containerManage/search.do'

        data={"warehouseCode":self.warehouseCode,
              "limit":"20",
              "draw":"3",
              "useState":"0"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["result"] == True:
            containerCode_list = re_json["rows"]
            containerCode = (random.sample(containerCode_list, 1))[0]["containerCode"]
            print("当前容器编码成功:" + str(containerCode))
            return containerCode
        else:
            print("查询容器编码失败" + re_result.text)

    def checkInputDate(self,barCode='',quantity=''):
        ##校验商品生产日期
        now_day = datetime.datetime.strptime(time.strftime("%Y%m%d", time.localtime()), '%Y%m%d')
        expireDate = (now_day + relativedelta(years=1)).strftime('%Y-%m-%d')

        url='http://jwmspre.cnsuning.com/jwms-web/unpackAccept/checkInputDate.do'

        data={"warehouseCode":self.warehouseCode,
              "receiveType":"1",
              "inputNo":self.logisticOrderId,
              "barCode":barCode,
              "productDate":time.strftime("%Y-%m-%d", time.localtime()),
              "dueDate":expireDate,
              "quantity":quantity}
        data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        print(data)
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        re_result = self.session.post(url=url, data=data.encode("utf-8"), headers=headers)
        re_json=json.loads(re_result.text)
        if re_json["message"]:
            print("校验商品生产日期成功:" + re_result.text)
        else:
            print("校验商品生产日期失败" + re_result.text)

    def bindWorkbench(self):
        ##拆包验收
        url='http://jwmspre.cnsuning.com/jwms-web/inOrder/bindWorkbench.do'

        data={"warehouseCode":self.warehouseCode,
              "workbenchCode":"BZ008"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["success"] == True:
            print("拆包验收登陆成功")
        else:
            print("拆包验收登陆失败" + re_result.text)

    def queryByInputNo(self):
        ##查询验收订单
        url='http://jwmspre.cnsuning.com/jwms-web/unpackAccept/queryByInputNo.do'

        data={"warehouseCode":self.warehouseCode,
              "receiptNo":self.logisticOrderId,   #逆向单号
              "receiveType":"1",
              "isRf":"false"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["result"] == True:

            print("查询验收订单成功")
            return re_json
        else:
            print("查询验收订单失败" + re_result.text)

    def searchSkuCode(self,cmmdtyCode=''):
        #查询商品条码
        url='http://jwmspre.cnsuning.com/jwms-web/base/newCmmdtyCollect/search.do'
        data={"sncmmdtyCode":cmmdtyCode}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            SkuCode = re_json["data"]["datas"][0]["barCode"]
            print("获取商品条码成功：" + str(SkuCode))
            return SkuCode
        else:
            print("获取商品条码失败：" + re_result.text)

    def searchCancleInfo(self):
        #查询销退通知单
        url='http://jwmspre.cnsuning.com/jwms-web/returnOrderNotification/search.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.logisticOrderId,
              "draw":"3",
              "offset":"0",
              "limit":"10"}
        cut=0
        while cut!=600:
            re_result = self.session.post(url=url, data=data, headers=self.headers)
            # print(re_result.text)
            re_json = json.loads(re_result.text)
            if not re_json["data"]["datas"]:
                print("未查询到退货通知单" + str(cut))
                time.sleep(10)
                cut = cut + 10
            elif re_json["data"]["datas"][0]["logisticOrderId"]==self.logisticOrderId:
                print("查询销退通知单成功")
                break
            else:
                print("查询销退通知单失败：" + re_result.text)
                break

    def queryNotificationDetails(self):
        #查询逆向单详情
        url='http://jwmspre.cnsuning.com/jwms-web/inOrderNotification/queryNotificationDetails.do'
        data={"orderNotificationNo":self.logisticOrderId,
              "warehouseCode":self.warehouseCode}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            orderId = re_json["data"]["details"][0]["id"]
            orderType = re_json["data"]["inOrderNotification"]["orderType"]
            ownerCode = re_json["data"]["inOrderNotification"]["ownerCode"]
            print("查询逆向单详情成功：" + str(orderId) + ';' + str(orderType) + ';' + str(ownerCode))
            return orderId, orderType,ownerCode
        else:
            print("查询逆向单详情失败：" + re_result.text)

    def updateStorehouseValue(self,DetailsInfo=''):
        DetailsInfo = list(DetailsInfo)
        orderId=DetailsInfo[0]
        orderType=DetailsInfo[1]
        ownerCode = DetailsInfo[2]
        details = [{"id":orderId,"orderNotificationNo":self.logisticOrderId,"storehouseCode":"NJ1","deficientStorehouseCode":"NJ2","ownerCode":ownerCode,"warehouseCode":self.warehouseCode}]
        #保存仓库信息
        url='http://jwmspre.cnsuning.com/jwms-web/inOrderNotification/updateStorehouseValue.do'
        data={"logisticOrderId":self.logisticOrderId,
              "orderType":orderType,
              "details":str(details)}
        print(data)
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["message"]=="保存成功":
            print("保存仓库信息成功")
            return orderId,orderType,ownerCode
        else:
            print("保存仓库信息失败：" + re_result.text)

    def getReceiveDetail(self,barCode):
        #输入商品条码
        url='http://jwmspre.cnsuning.com/jwms-web/unpackAccept/getReceiveDetail.do'
        data={"warehouseCode":self.warehouseCode,
              "receiveNo":self.logisticOrderId,
              "barCode":barCode,
              "receiveType":"1"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["success"]==True:
            print("输入商品条码成功")
        else:
            print("输入商品条码失败：" + re_result.text)

    def saveContainerRecord(self,containerCode='',info='',barCode=''):
        #提交订单
        re_queryByInputNo = info
        cmmdtyCode = re_queryByInputNo["data"]["details"][0]["skuCode"]
        skuName = re_queryByInputNo["data"]["details"][0]["skuName"]
        vendorCode = re_queryByInputNo["data"]["details"][0]["vendorCode"]
        itemNumber = re_queryByInputNo["data"]["details"][0]["itemNumber"]
        ownerCode = re_queryByInputNo["data"]["details"][0]["ownerCode"]
        ownerName = re_queryByInputNo["data"]["details"][0]["ownerName"]
        normalTemporaryLocation = re_queryByInputNo["data"]["details"][0]["normalTemporaryLocation"]
        quantity = int(re_queryByInputNo["data"]["details"][0]["qtySku"])
        gmtBegin = int(time.time() * 1000)

        now_day = datetime.datetime.strptime(time.strftime("%Y%m%d", time.localtime()), '%Y%m%d')
        expireDate = (now_day + relativedelta(years=1)).strftime('%Y-%m-%d')
        url='http://jwmspre.cnsuning.com/jwms-web/unpackAccept/saveContainerRecord.do'
        data={
              "logisticOrderId": self.logisticOrderId,
              "warehouseCode": self.warehouseCode,
              "receiveType": "1",
              "expressCode": "",
              "record": {
                "containerCode": containerCode,
                "warehouseCode": self.warehouseCode,
                "orderType": "ZCRE",
                "purpose": "XTSH",
                "status": 1,
                "gmtBegin": gmtBegin,
                "expressCode": "",
                "originOrderNo": self.logisticOrderId,
                "refTaskNo": "",
                "isForciblyReceived": "1"
              },
              "details": [
                {
                  "detail": {
                    "skuCode": str(cmmdtyCode),
                    "skuName": str(skuName),
                    "warehouseCode": self.warehouseCode,
                    "ownerCode": str(ownerCode),
                    "ownerName": str(ownerName),
                    "storehouseCode": "NJ1",
                    "storehouseName": "3C",
                    "temporaryZone": "3CXT",
                    "temporaryLocation": str(normalTemporaryLocation),
                    "barCode": barCode,
                    "lotNumber": "",
                    "skuStateAttr": "1",
                    "bestq": "",
                    "quantity": str(quantity),
                    "workbench": "BZ008",
                    "itemNumber": str(itemNumber),
                    "insmk": "",
                    "isBunch": 0,
                    "productDate": time.strftime("%Y-%m-%d", time.localtime()),
                    "expireDate": expireDate,
                    "vendorCode": str(vendorCode)
                  },
                  "serialNoList": [
                    {
                      "isSerialNo": "-1",
                      "serialNo": "",
                      "skuCode": str(cmmdtyCode),
                      "skuName": str(skuName)
                    }
                  ]
                }
              ]
            }

        data = json.dumps(data,ensure_ascii=False,separators=(',',':'))
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        re_result = self.session.post(url=url, data=data.encode("utf-8"), headers=headers)
        re_json = json.loads(re_result.text)
        if re_json["success"]==True:
            print("订单提交成功")
        else:
            print("订单提交失败：" + re_result.text)

    def closeCompleteContainer(self,containerCode=''):
        #保存容器
        url='http://jwmspre.cnsuning.com/jwms-web/unpackAccept/closeCompleteContainer.do'
        data={"warehouseCode":self.warehouseCode,
              "containerCode":containerCode}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["success"]==True:
            print("完成容器成功")
        else:
            print("完成容器失败：" + re_result.text)

    def querySerialNoPrint(self):
        #打印
        url='http://jwmspre.cnsuning.com/jwms-web/returnOrderNotification/querySerialNoPrint.do'
        data={"warehouseCode":self.warehouseCode,
              "orderNotificationNos":self.logisticOrderId}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        print("打印：" + re_result.text)

    def newSearch(self):
        #查询单据状态
        url='http://jwmspre.cnsuning.com/jwms-web/report/orderStatusDetail/newSearch.do'
        data={"warehouseCode":self.warehouseCode,
              "orderNo":self.logisticOrderId,
              "types":"1"}
        cut = 0
        state = "0"
        while cut!=60:
            re_result = self.session.post(url=url, data=data, headers=self.headers)
            re_json = json.loads(re_result.text)
            if re_json["result"]==True:
                for i in re_json["data"]["datas"]:
                    print(i["statusDesc"])
                    if i["statusDesc"]=="仓库入库":
                        state = "1"
                if state =="0":
                    time.sleep(5)
                    cut = cut + 5
                    continue
                else:
                    print("退货销单成功")
                    break
            else:
                print("退货销单失败：" + re_result.text)

class OmsdBack():
    def __init__(self,warehouseCode='L025',omsOrderNo=''):
        self.warehouseCode=warehouseCode
        self.omsOrderNo=omsOrderNo
        self.session=requests.session()
        Request_URL = 'https://ssopre.cnsuning.com/ids/login'
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        login_data = {
            "service": "http://omsdbackpre.cnsuning.com:8080/omsd-web-in/auth?targetUrl=http%3A%2F%2Fomsdbackpre.cnsuning.com%3A8080%2Fomsd-web-in%2Findex.htm%3FsnapshotId%3DD42D00499FCFC37C6E4AF9116811FB83",
            "uuid": "0c8f502b-c238-44dc-9779-7e4195410ca5",
            "loginTheme": "omsdbackpre.cnsuning.com:8080",
            "username": "88210832",
            "password2": "IsLHRlqvf/90rXpNHd4+BYPSsJ4cQBvyc6OE/+V/rVcurzG8uN1gROK7e7NKGAnxbB6n7bK74xlijVQYiSD4Ok9/g4zPi7IWeK+lx3Z0ImynMjmokY02TBQSeX6PDpxtCeA4fqSNbPszweL0b5LH8H3R4XgwFeXpRsAjUwrfHUU=",
        }
        self.login_result = self.session.post(Request_URL, data=login_data, headers=self.headers)

    def queryHeader(self):
        ##查询订单信息
        url='http://omsdbackpre.cnsuning.com:8080/omsd-web-in/orderDetail/queryHeader.htm'
        data={"orderItemId":self.omsOrderNo,
              "billType":"1"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        if re_result.status_code==200:
            re_json = json.loads(re_result.text)
            orderId = re_json["OrderHeaderDTO"]["orderId"]
            return orderId
        else:
            print("查询订单信息失败失败" + re_result.text)

    def pageQuery(self,orderId):
        ##查询逆向oms行号
        url='http://omsdbackpre.cnsuning.com:8080/omsd-web-in/orderDetail/pageQuery.htm'
        data={"orderId":orderId,
              "billType":"1",
              "pageNumber":"1",
              "pageSize":"10"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        omsNo = ""
        if isinstance(re_json["1"],list):
            for i in re_json["1"]:
                if i["BILL_TYPE"]==-1 and i["STATUS_CODE_IS"]=="15":
                    omsNo = i["ORDER_ITEM_ID"]
                    print("查询逆向oms行号成功：" + str(omsNo))
                    return omsNo
            if omsNo=="":
                print("未查询到逆向oms行号，请确认云客服是否已审核通过")
        else:
            print("查询逆向oms行号失败" + re_result.text)

    def creatOrdiDeli(self):
        ##生成逆向发货指令
        url='http://omsdbackpre.cnsuning.com:8080/omsd-web-in/orderDeli/creatOrdiDeli.htm'

        data={"orderItemId":self.omsOrderNo,
              "planOutTime":time.strftime("%Y-%m-%d", time.localtime()),
              "billType":"-1"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["RETCODE"] =="SUCCESS":
            print("生成发货指令成功")
        else:
            print("生成发货指令失败" + re_result.text)

class returnGoods():
    def __init__(self):
        pass

    def returnGoodsfun(self,omsOrderNo):
        sendOMS = OmsdBack(omsOrderNo=omsOrderNo)

        orderId = sendOMS.queryHeader()
        backOmsNo = sendOMS.pageQuery(orderId)  # 查询逆向oms行号
        sendOMS.creatOrdiDeli()  # 生成发货指令

        logisticOrderId = "OMS" + backOmsNo + "01"
        data_init = FuncBase(logisticOrderId=logisticOrderId)  # 初始化方法

        data_init.searchCancleInfo()  # 查询销退通知单
        DetailsInfo = data_init.queryNotificationDetails()  # 查询退货订单详情

        data_init.updateStorehouseValue(DetailsInfo=DetailsInfo)  # 库存信息保存

        data_init.bindWorkbench()  # 拆包验收登陆
        re_queryByInputNo = data_init.queryByInputNo()  # 查询验收订单
        cmmdtyCode = re_queryByInputNo["data"]["details"][0]["skuCode"]  # 商品编码

        barCode = data_init.searchSkuCode(cmmdtyCode=cmmdtyCode)  # 查询商品条码
        data_init.getReceiveDetail(barCode=barCode)  # 输入条码
        containerCode = data_init.queryVess()  # 查询容器编码
        # quantity = re_queryByInputNo["data"]["details"][0]["qtySku"]  #退货数量
        # data_init.checkInputDate(barCode=barCode, quantity=quantity)   #校验商品生产日期
        data_init.saveContainerRecord(containerCode=containerCode, info=re_queryByInputNo, barCode=barCode)  # 提交订单
        data_init.closeCompleteContainer(containerCode=containerCode)  # 完成容器
        data_init.newSearch()  # 查询单据

if __name__ == '__main__':

    ##需要云客服审核通过后才能执行退货脚本

    omsOrderNo='35105641052301'

    returnGoods().returnGoodsfun(omsOrderNo)

