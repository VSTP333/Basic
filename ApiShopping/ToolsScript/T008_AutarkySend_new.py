#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: T008_AutarkySend_new.py
@time: 2019-11-07 15:23:23
@desc:新自营发货脚本，支持一行多包裹发货
'''

import requests
import json,time,redis,calendar
import random

class FuncBase():
    def __init__(self,warehouseCode='L025',OMSITEM=''):
        day_now = time.localtime()
        self.month = day_now.tm_mon
        self.warehouseCode=warehouseCode
        self.OMSITEM=OMSITEM
        self.session=requests.session()
        Request_URL = 'https://uiapre.cnsuning.com/ids/login'
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        login_data = {
            "service": "http://jwmspre.cnsuning.com/jwms-web/auth?targetUrl=http%3A%2F%2Fjwmspre.cnsuning.com%2Fjwms-web%2Findex.html",
            "uuid": "bd8022a3-dfff-42b8-89d9-d1e33c0f1595",
            "loginTheme": "portal",
            "username": "18063468",
            "password": "18063468",
        }
        self.login_result = self.session.post(Request_URL, data=login_data, headers=self.headers)

    def choseSta(self,linkCode):
        if linkCode == 'toBeAllocated':
            orderSta = '待分配'
        elif linkCode == 'quickAllocated':
            orderSta = '分配完成'
        elif linkCode == 'quickReChecking':
            orderSta = '包装复核中'
        elif linkCode == 'quickReCheckSucceed':
            orderSta = '复核完成'
        elif linkCode == 'quickForwarded':
            orderSta = '出库成功'
        elif linkCode == 'allocated':
            orderSta = '分配已完成'
        elif linkCode == 'allocateFailed' or linkCode == 'pickTaskCreated' or linkCode == 'picked' or linkCode == 'forwarded':
            print("当前订单状态为：" + linkCode + ",请使用老发货脚本")
        else:
            print("订单状态未知：" + linkCode)
            exit()
        return orderSta

    def queryAssigned(self):
        ##销售订单管理查询订单状态
        day_now = time.localtime()
        wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 返回为此月天数
        day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)  # 月末日期
        month = day_now.tm_mon
        end_day = int(time.strftime("%d", time.localtime())) + 1
        startSendEndDatetime = time.strftime("%Y-%m-%d", time.localtime(time.time() - 604800)) + " 00:00:00"
        if end_day <= monthRange:
            endSendEndDatetime = time.strftime("%Y-%m-%d", time.localtime(time.time() + 86400)) + " 23:59:59"
        else:
            endSendEndDatetime = day_end + " 23:59:59"
        url='http://jwmspre.cnsuning.com/jwms-web/out/outOrder/queryOutOrderDetailPage.do'

        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM,
              "month": str(month),
              "startCreateDate": startSendEndDatetime,
              "endCreateDate": endSendEndDatetime,
              "offset":"0",
              "limit":"10"}
        cut=0
        while cut!=600:
            re_result=self.session.post(url=url,data=data,headers=self.headers)
            re_json=json.loads(re_result.text)
            if re_json["data"]["totalCount"] ==0:
                print("未查到订单数据，请稍等" + str(cut))
                time.sleep(10)
                cut = cut + 10
                continue
            else:
                if re_json["result"] == True:
                    linkCode = re_json["data"]["datas"][0]["linkCode"]   #状态编号
                    id = re_json["data"]["datas"][0]["id"]  #id
                    return linkCode,id
                else:
                    print("查询订单状态失败" + re_result.text)
                break

    def cancelDistribution(self,ids):
        ##取消分配
        url='http://jwmspre.cnsuning.com/jwms-web/out/outOrder/cancelDistribution.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderIds":self.OMSITEM,
              "ids":ids}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["success"] == True:
            print("取消分配成功")
        else:
            print("取消分配失败" + re_result.text)

    def searchOutOrder(self):
        ##查询订单状态
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/searchOutOrderHeaderPage.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM,
              "offset":"0",
              "limit":"10"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["result"] == True:
            linkCode = re_json["data"]["datas"][0]["linkCode"]  # 订单状态
            order_id = re_json["data"]["datas"][0]["id"]  # 订单id
            order_status = self.choseSta(linkCode)
            return order_status,order_id
        else:
            print("查询订单状态失败" + re_result.text)

    def checkCkzt(self):
        #查询交货单信息
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/checkCkzt.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["result"]==True:
            print("查询交货单信息成功")
        else:
            print("查询未释放波次失败:" + re_result.text)

    def checkOrderModeWork(self):
        #查询订单类型checkOrderModeWork
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/checkOrderModeWork.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"] == True:
            print("查询订单类型checkOrderModeWork成功")
        else:
            print("查询订单类型checkOrderModeWork失败" + re_result.text)

    def queryOutOrderHeader(self,order_id):
        #查询出库订单信息ById
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/queryOutOrderHeaderById.do'
        data = {"warehouseCode": self.warehouseCode,
                "id": order_id,
                "month": str(self.month),
                "jsoncallback": "true"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            print("查询出库订单信息成功")
            return re_json
        else:
            print("查询出库订单信息ById失败:"+re_result.text)

    def OutOrderProduct(self,order_id='',bolCode='',busWorkMode=''):
        #查询商品信息
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/queryOutOrderProductByCode.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM,
              "headId":order_id,
              "bolCode":bolCode,
              "busWorkMode":busWorkMode,
              "month":str(self.month),
              "offset":"0",
              "limit":"-1"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            print("查询商品信息成功")
            return re_json
        else:
            print("查询商品信息失败：" + re_result.text)

    def checkZ4Order(self):
        #查询订单信息checkZ4Order
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/checkZ4Order.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["status"] == 1:
            print("查询订单信息checkZ4Order成功")
        else:
            print("查询订单信息checkZ4Order失败：" + re_result.text)

    def queryPredistribution(self,productId,busWorkMode,skuCode):
        #预分配
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/queryPredistribution.do'
        data={"warehouseCode":self.warehouseCode,
              "month":str(self.month),
              "skuCode": skuCode,
              "productId":productId,
              "busWorkMode":busWorkMode,
              "offset":"0",
              "limit":"-1"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["data"]:
            print("预分配成功")
            return re_json
        else:
            print("预分配失败" + re_result.text)

    def updateDistribution(self,info='',bolCode='',busWorkMode='',productId='',order_id='',amount=0):
        #库存分配
        inventoryId = ""
        for i in info["data"]:
            # if i["zoneCode"]=="3CC" and i["availableQuantity"]>=amount:
            if i["availableQuantity"] >= amount:
                inventoryId = i["id"]
                skuCode = i["skuCode"]
                ownerCode = i["ownerCode"]
                skuProp = i["skuProp"]
                storehouseCode = i["storehouseCode"]
                zoneCode = i["zoneCode"]
                locationCode = i["locationCode"]
                break
        if inventoryId=="":
            print("没有可用库存信息")
            exit()

        inventoryInfo = {str(productId):[{"inventoryId":inventoryId,"skuCode":skuCode,
                                     "logisticOrderId":self.OMSITEM,"wbsUnit":ownerCode,"headId":str(order_id),
                                     "stockType":"","warehouseCode":self.warehouseCode,"storehouseCode":storehouseCode,"zoneCode":zoneCode,
                                     "locationCode":locationCode,"ownerCode":ownerCode,"dueDate":None,"batchNo":"",
                                     "blpSerialNum":None,"skuProp":skuProp,"Takeup":str(amount)}]}

        inventoryInfo = json.dumps(inventoryInfo, ensure_ascii=False, separators=(',', ':'))

        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/updateDistribution.do'
        # headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        data={"warehouseCode":self.warehouseCode,
              "month":str(self.month),
              "bolCode":bolCode,
              "logisticOrderId":self.OMSITEM,
              "shipmentNo":"null",
              "busWorkMode":busWorkMode,
              "inventoryInfo":inventoryInfo}

        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["success"]==True:
            print("库存分配成功")
        else:
            print("库存分配失败" + re_result.text)

    def queryPackage(self,bolCode=''):
        #查询包裹
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/queryPackage.do'
        data={"warehouseCode":self.warehouseCode,
              "bolCode":bolCode,
              "month":str(self.month),
              "logisticOrderId":self.OMSITEM}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            print("查询包裹成功")
        else:
            print("查询包裹失败" + re_result.text)

    def createPackage(self,bolCode='',headId='',order_id='',material='',materialDesc='',num='',serialnos=''):
        #创建包裹

        details =[{"id":headId,"skuCode":material,"skuName":materialDesc,"logisticOrderId":self.OMSITEM,"ownerCode":"R5400","headId":order_id,"stockType":"","warehouseCode":self.warehouseCode,"amount":num,"serialnos":serialnos}]
        details = json.dumps(details, ensure_ascii=False, separators=(',', ':'))
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/createPackage.do'
        data={"warehouseCode":self.warehouseCode,
              "bolCode":bolCode,
              "headId":order_id,
              "logisticOrderId":self.OMSITEM,
              "month":str(self.month),
              "details":details}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"] == True:
            expressCode = re_json["data"]["expressCode"]
            print("包装复核成功,包裹号：" + expressCode)
            return expressCode
        else:
            print("包装复核失败：" + re_result.text)

    def printSheet(self,expressCodes,bolCode):
        #打印出库单
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/printSheet.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM,
              "expressCodes":expressCodes,
              "bolCode":bolCode}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["success"]==True:
            print("打印出库单成功")

        else:
            print("打印出库单失败：" + re_result.text)

    def printBill(self):
        #打印发票
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/printBill.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM,
              "month":self.month,
              "isPrintBill":"1"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        print("打印发票：" + re_result.text)

    def queryOutPackage(self):
        #查询包裹号
        url='http://jwmspre.cnsuning.com/jwms-web/out/outPackage/queryOutPackage.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        expressCode = []
        if re_json["result"]==True:
            for i in re_json["data"]:
                expressCode.append(i["expressCode"])
            print("包裹号：" + str(expressCode))
            return expressCode
        else:
            print("查询包裹号失败：" + re_result.text)

    def queryPackageAndWuliu(self,order_id='',busWorkMode=''):
        #查询包裹详细信息
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/queryPackageAndWuliu.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM,
              "headId":order_id,
              "month":self.month,
              "busWorkMode":busWorkMode}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            expressCode = re_json["data"][0]["expressCode"]
            print("查询包裹详细信息成功")
            return expressCode
        else:
            print("查询包裹详细信息失败：" + re_result.text)

    def updateSendLogistic(self,bolCode=''):
        #确认出库操作
        url='http://jwmspre.cnsuning.com/jwms-web/quickOutOrder/updateSendLogisticOrder.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM,
              "bolCode":bolCode,
              "month":self.month}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            print("确认出库操作成功")
        else:
            print("确认出库操作失败：" + re_result.text)

    def getPrintTemplate(self):
        #获取打印模板
        url='http://jwmspre.cnsuning.com/jwms-web/inOrderNotification/getPrintTemplate.do'
        data={"templateName":"ZLESWM_301.html"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        if re_result.status_code==200:
            print("获取打印模板成功")
        else:
            print("获取打印模板失败：" + re_result.text)

class SendGoods(FuncBase):

    def updateDis(self,order_id=''):
        #分配库存
        print("*************开始分配库存*************")
        # self.checkCkzt()             #查询交货单信息
        # self.checkZ4Order()          #查询订单信息checkZ4Order
        # self.checkOrderModeWork()    #查询订单类型checkOrderModeWork
        outOrder_info = self.queryOutOrderHeader(order_id)        #查询出库订单信息
        bolCode = outOrder_info["data"]["bolCode"]     #合单号
        busWorkMode = outOrder_info["data"]["busWorkMode"]     #订单类型
        skuCode = outOrder_info["data"]["material"]        #商品sku
        amount = outOrder_info["data"]["amount"]    #商品数量
        prod_info = self.OutOrderProduct(order_id,bolCode,busWorkMode)   #查询商品信息
        productId = prod_info["data"][0]["id"]

        product_info = self.queryPredistribution(productId,busWorkMode,skuCode)  #预分配
        self.updateDistribution(product_info,bolCode,busWorkMode,productId,order_id,int(amount))   #库存分配


    def createPackages(self,order_id='',num='',serNo=''):
        #包装复核

        print("*************开始包装复核*************")
        # self.checkZ4Order()          #查询订单信息checkZ4Order
        outOrder_info = self.queryOutOrderHeader(order_id)  # 查询出库订单信息
        bolCode = outOrder_info["data"]["bolCode"]      # 合单号
        busWorkMode = outOrder_info["data"]["busWorkMode"]  # 订单类型
        prod_info = self.OutOrderProduct(order_id, bolCode, busWorkMode)  # 查询商品信息
        productId = prod_info["data"][0]["id"]           #商品id
        material = prod_info["data"][0]["material"]  # 商品sku
        materialDesc = prod_info["data"][0]["materialDesc"]   #商品名称
        amount = prod_info["data"][0]["amount"]    #商品数量
        checkAmount = prod_info["data"][0]["checkAmount"]  #已复核数量
        serialnos_count = ""
        if serNo =='Y':   #判断是否绑定串码
            serNo = SernrNo()
            for i in range(int(amount)):
                ser_info = serNo.getskuCode(skuid=material)
                serialnos = serNo.addConfirm(info=ser_info)
                if i == 0:
                    serialnos_count = serialnos
                else:
                    serialnos_count = serialnos_count + "," + serialnos

        if num=="0":
            num = str(int(amount))
        for i in num.split(","):
            # self.queryPackage(bolCode)  ##查询包裹
            print("订单行商品总数量："+ str(int(amount)))
            print("已复核数量：" + str(int(checkAmount)))
            print("当前要复核数量：" + str(i))
            if int(amount)==int(checkAmount):
                break
            elif int(i)<=(int(amount)-checkAmount):
                expressCodes = self.createPackage(bolCode, productId,order_id,material,materialDesc,i,serialnos_count)   #创建包裹
                self.printSheet(expressCodes, bolCode)       #打印出库单
                # self.printBill()   #打印发票
                # self.queryPackage(bolCode)  ##查询包裹
                prod_info = self.OutOrderProduct(order_id, bolCode, busWorkMode)  # 查询商品信息
                checkAmount = prod_info["data"][0]["checkAmount"]  # 已复核数量
                # self.getPrintTemplate()   #获取打印模板
                time.sleep(3)
            else:
                print("当前要复核数量大于未复核数量，请检查")
                exit()

    def sendLogistic(self):
        #确认出库
        print("*************开始确认出库*************")
        order_status, order_id = self.searchOutOrder()  # 查询订单状态
        if order_status == "复核完成":
            # self.checkZ4Order()  # 查询订单信息checkZ4Order
            outOrder_info = self.queryOutOrderHeader(order_id)  # 查询出库订单信息
            busWorkMode = outOrder_info["data"]["busWorkMode"]  # 订单类型
            bolCode = outOrder_info["data"]["bolCode"]  # 合单号
            self.queryPackageAndWuliu(order_id, busWorkMode)   #查询包裹详细信息
            self.updateSendLogistic(bolCode)  #确认出库操作
        else:
            print("当前状态无法确认出库：" + order_status)
            exit()

class SernrNo(FuncBase):
    def getskuCode(self, skuid):
        ##获取商品信息
        url = 'http://jwmspre.cnsuning.com/jwms-web/lsws/libraryManager/getskuCode.do'
        data = {"warehouseCode": self.warehouseCode,
                "ownerCode": 'R5400',
                "sncmmdtyCode": skuid}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["info"] != {}:
            print("获取商品信息成功")
            return re_json
        else:
            print("获取商品信息失败" + re_result.text)

    def addConfirm(self, info):
        ##绑定串码
        skuid = info["info"]["sncmmdtyCode"]
        arrSerialNumber = "SN" + str(int(time.time()*10000))
        skuname = info["info"]["cmmdtyName"]
        url = 'http://jwmspre.cnsuning.com/jwms-web/lsws/libraryManager/addConfirm.do'
        data = {"warehouseCode": self.warehouseCode,
                "ownerCode": 'R5400',
                "sncmmdtyCode": skuid,
                "arrSerialNumber[]":arrSerialNumber,
                "cmmdtyName":skuname,
                "warehouseName":"苏宁南京中心仓",
                "storageType":"01"
                }
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["success"] == True:
            print("绑定串码成功" + arrSerialNumber)
            return arrSerialNumber
        else:
            print("绑定串码失败" + re_result.text)


class Access():
    def __init__(self):
        self.session=requests.session()
        Request_URL = 'http://edsadminpre.cnsuning.com/eds-admin-web/user/p/submit.action'
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        login_data = "userId=sysadmin&pwd=123456qq"
        self.login_result = self.session.post(Request_URL, data=login_data, headers=self.headers)

class Logistic():
    def __init__(self,OMSITEM):
        self.user = '15073894'
        self.OMSITEM = OMSITEM
        self.session = requests.session()
        url1 = 'http://edspre.cnsuning.com/eds-web/user/p/login.action'
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}

        login_result = self.session.get(url=url1, headers=self.headers)
        cookies=login_result.cookies["JSESSIONID"]
        url2='http://edspre.cnsuning.com/eds-web/img/p/createImg.action'
        self.session.get(url=url2,headers=self.headers)  #刷新验证码
        res_key = "YWL:PUMP:CAPPRO_CMD" + str(cookies)

        redis1 = redis.Redis(host='10.27.113.6', port=6379, db=0)
        Code = redis1.get(res_key)
        if Code is None:
            redis2 = redis.Redis(host='10.27.113.21', port=6379, db=0)
            Code = redis2.get(res_key)
        url3='http://edspre.cnsuning.com/eds-web/user/p/submit.action'
        login_data = {"userId":self.user,
                      "verifyCode":Code.decode('utf-8'),
                      "password1":"bc6awyMiRejNgJz2V4B2UyWyngJbhI7Cki2lOG/2GHCStYcAaNWqrEU9NHMzCpjWNN6nIuOpS1jtDdMxCrhVpUE/WS3SQ3HdfTKrG5wsYy2851K0OxDFCJRkMV26C4ZVwCBo5Yn56Y7hrOG7FOR00SP5x57/Wr8HEMsrWqXCt4o="}
        self.session.post(url=url3,data=login_data,headers=self.headers)

    def daoJian(self,expressCode):
        #到件
        url='http://edspre.cnsuning.com/eds-web/daojianForWeb/profile/daojian.action'
        for i in expressCode:
            data={"goodsType":"0",
                  "scanType":"03",
                  "lastSiteId": "L025",
                  "factory": "L025",
                  "wayBillNo": i,
                  "version": "PC",
                  "imei": self.user,
                  "siteId": "K025010401",
                  "userId": self.user,
                  "lastSiteName": "苏宁南京分拨中心1",
                  "confirm": "Y",
                  "inOut": "I",
                  "zybsFlag": "Y",
                  "frontFrom": "1",
                  "jsoncallback": "true"}
            cut = 0
            while cut!=600:
                re_result = self.session.post(url=url, data=data, headers=self.headers)
                re_json = json.loads(re_result.text)
                if re_json["message"]:
                    if re_json["message"]=="已入站" or re_json["message"]=="成功":
                        print("到件成功")
                        time.sleep(3)
                        break
                    elif re_json["message"]=="请使用扫描员收件操作":
                        break
                    else:
                        print("到件查询失败" + str(cut))
                        time.sleep(10)
                        cut = cut +10
                else:
                    print("到件失败：" + re_result.text)
                    break

    def queryStationDriver(self):
        # 获取配送员
        url = 'http://edspre.cnsuning.com/eds-web/deliveryoffstation/profile/queryStationDriver.action'
        headers={"Content-Type":"application/json"}
        re_result = self.session.post(url=url,headers=headers)
        re_json = json.loads(re_result.text)
        if re_json["data"]!=[]:
            Drivers_List=re_json["data"]
            Drivers = random.sample(Drivers_List, 1)
            print("获取配送员成功：" + str(Drivers[0]["PQRYXM"]))
            time.sleep(5)
            return Drivers[0]["PQRYBH"]
        else:
            print("获取配送员失败：" + re_result.text)

    def scanPackageWoi(self,packageNo):
        #获取包裹信息
        url='http://edspre.cnsuning.com/eds-web/deliveryoffstation/profile/scanPackageWoi.action'
        data={"packageNo":packageNo[0],
              "checkBol":"flase"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            print("获取包裹信息成功")
        else:
            print("获取包裹信息失败：" + re_result.text)

    def doOffStationWoi(self,userId=''):
        #配送离站
        while 1:
            url='http://edspre.cnsuning.com/eds-web/deliveryoffstation/profile/doOffStationWoi.action'
            data={"dnos":self.OMSITEM,
                  "userId":userId,
                  "operator": self.user}
            re_result = self.session.post(url=url, data=data, headers=self.headers)
            re_json = json.loads(re_result.text)
            if re_json["returnCode"] == "E":
                print("配送员信息缺失，重新选择配送员")
                userId = self.queryStationDriver()  # 获取配送员
                continue
            elif re_json["returnCode"]=="S":
                shpmntno = re_json["list"]["zylist"]  # 装运编号
                print("配送离站成功")
                time.sleep(5)
                return shpmntno
            else:
                print("配送离站失败：" + re_result.text)
                exit()


    def saveBillcancel(self,shpmntno='',expressCode='',operateType=''):
        #销单
        if operateType=='access':
            cancelType='0001'
            ztype='1000'
            operate='妥投'
        else:
            cancelType='0003'
            ztype='3003'
            operate='拒收'
        url='http://edspre.cnsuning.com/eds-web/backtoStation/profile/saveBillcancel.action'

        data={"delivery":self.OMSITEM,
              "shpmntno":shpmntno,
              "amountpayment": "0",
              "factory": "L025",
              "packagecustomer": expressCode,
              "orderType": "1",
              "cancelType": cancelType,
              "ztype": ztype,
              "brqs": "on"}

        re_result = self.session.post(url=url, data=data, headers=self.headers)

        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            print(operate + "操作成功")
        else:
            print(operate + "操作失败：" + re_result.text)

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


    def pageQuery(self):
        ##查询逆向oms行号
        url='http://omsdbackpre.cnsuning.com:8080/omsd-web-in/orderDetail/pageQuery.htm'
        data={"orderId":self.omsOrderNo[0:-2],
              "billType":"1",
              "pageNumber":"1",
              "pageSize":"10"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["data"] ==0:
            print("查询逆向oms行号成功：")
        else:
            print("查询逆向oms行号失败" + re_result.text)

    def creatOrdiDeli(self):
        ##生成发货指令
        url='http://omsdbackpre.cnsuning.com:8080/omsd-web-in/orderDeli/creatOrdiDeli.htm'

        data={"orderItemId":self.omsOrderNo,
              "planOutTime":time.strftime("%Y-%m-%d", time.localtime()),
              "billType":"1"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["RETCODE"] =="SUCCESS":
            print("生成发货指令成功")
        else:
            print("生成发货指令失败" + re_result.text)

class sendGoodsjob():
    def __init__(self):
        pass
    def send(self,omsOrderNo,operateType,num,serNo):
        sendOMS = OmsdBack(omsOrderNo=omsOrderNo)
        sendOMS.creatOrdiDeli()  # 生成发货指令

        OMSITEM = "OMS" + omsOrderNo + "01"
        data_init = FuncBase(OMSITEM=OMSITEM)
        send = SendGoods(OMSITEM=OMSITEM)

        linkCode,ids = data_init.queryAssigned()   #查询订单初识状态
        order_status = data_init.choseSta(linkCode)

        if order_status=="分配已完成":
            data_init.cancelDistribution(ids)   #取消分配

        order_status,order_id = data_init.searchOutOrder()  # 查询订单状态
        print("当前订单状态为：" + order_status)

        if order_status == "待分配":
            send.updateDis(order_id)     # 分配库存
            send.createPackages(order_id,num,serNo)     # 包装复核
            send.sendLogistic()           #确认出库

        elif order_status == "分配完成" or order_status == "包装复核中":
            send.createPackages(order_id, num,serNo)  # 包装复核
            send.sendLogistic()  # 确认出库

        elif order_status == "复核完成":
            send.sendLogistic()  # 确认出库

        if operateType!="out":
            outtime = 0  # 初始化超时时间
            while outtime != 600:
                time.sleep(5)
                order_status, order_id = data_init.searchOutOrder()  # 查询订单状态
                print("当前订单状态:" + str(order_status) + str(outtime))
                if order_status == "出库成功":
                    expressCode = send.queryOutPackage()  ##查询包裹
                    logistic = Logistic(OMSITEM=OMSITEM)
                    logistic.daoJian(expressCode=expressCode)  # 到件
                    time.sleep(60)
                    Driver = logistic.queryStationDriver()  # 获取配送员
                    logistic.scanPackageWoi(packageNo=expressCode)  # 获取包裹信息
                    shpmntno = logistic.doOffStationWoi(userId=Driver)  # 配送离站
                    logistic.saveBillcancel(shpmntno=shpmntno,expressCode=expressCode,operateType=operateType)  ##销单
                    break
                time.sleep(10)
                outtime = outtime + 10
        else:
            print("**********发货完成**********")

if __name__ == '__main__':

    omsOrderNo='00105640891301'

    operateType = "access"  ##发货-out  妥投-access    拒收-reject

    num = "0"    #分包裹数量，例：1,1,1  则分3个包裹，每个包裹各1个
                     #不分包裹则传0
    serNo = "Y"      #是否绑定串码

    sendGoodsjob().send(omsOrderNo,operateType,num,serNo)