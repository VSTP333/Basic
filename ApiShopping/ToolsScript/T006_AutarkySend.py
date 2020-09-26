#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: T006_AutarkySend.py
@time: 2019-10-23 16:47:01
@desc: 自营发货脚本
'''

import requests
import json,time,redis,calendar
import random

class FuncBase():
    def __init__(self,warehouseCode='L025',OMSITEM=''):
        self.warehouseCode=warehouseCode
        self.OMSITEM=OMSITEM
        self.session=requests.session()
        Request_URL = 'https://ssopre.cnsuning.com/ids/login'
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        login_data = {
            "service": "http://jwmspre.cnsuning.com/jwms-web/auth?targetUrl=http%3A%2F%2Fjwmspre.cnsuning.com%2Fjwms-web%2Findex.html",
            "uuid": "bd8022a3-dfff-42b8-89d9-d1e33c0f1595",
            "loginTheme": "portal",
            "username": "15030108",
            "password": "15030108",
        }
        self.login_result = self.session.post(Request_URL, data=login_data, headers=self.headers)
    def choseSta(self,linkCode):

        if linkCode == 'toBeAllocated':
            orderSta = '待分配'
        elif linkCode == 'allocated':
            orderSta = '分配成功'
        elif linkCode == 'allocateFailed':
            orderSta = '分配失败'
        elif linkCode == 'pickTaskCreated':
            orderSta = '拣选单创建成功'
        elif linkCode == 'picked':
            orderSta = '已拣选'
        elif linkCode == 'forwarded':
            orderSta = '已发运'
        else:
            orderSta = "订单状态未知：" + linkCode
        return orderSta

    def queryAssigned(self):
        ##查询订单状态
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
                    orderSta = self.choseSta(linkCode=linkCode)    #订单状态
                    bolCode = re_json["data"]["datas"][0]["bolCode"]  #合单号
                    return orderSta,bolCode
                else:
                    print("查询订单状态失败" + re_result.text)
                break

    def queryBolCode(self,bolCode=''):
        #查询合单号
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
              "bolCode":bolCode,
              "month":str(month),
              "offset": "0",
              "limit": "10",
              "startCreateDate":startSendEndDatetime,
              "endCreateDate":endSendEndDatetime}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        orderNo_dict={}
        if re_json["result"] == True:
            for i in re_json["data"]["datas"]:
                orderSta = self.choseSta(linkCode=i["linkCode"])    #订单状态
                print("合单号有：" + i["logisticOrderId"] + " " + str(orderSta))
                orderNo_dict[i["logisticOrderId"]] = orderSta
        else:
            print("查询合单号失败" + re_result.text)
        return orderNo_dict

    def queryOrderRepertory(self,order_no=''):
        #查询库存分配详情
        if order_no=="":
            order_no=self.OMSITEM
        url='http://jwmspre.cnsuning.com/jwms-web/out/orderRepertoryDistribution/queryOrderRepertoryDistributionPage.do'
        data={"warehouseCode":self.warehouseCode,
              "month":"",
              "offset": "0",
              "limit": "10",
              "logisticOrderId":order_no}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["result"] == True:
            return re_json
        else:
            print("查询库存分配详情失败" + re_result.text)

    def assignedOrder(self,order_no):
        #库存分配
        if order_no=="":
            order_no=self.OMSITEM
        url='http://jwmspre.cnsuning.com/jwms-web/out/orderRepertoryDistribution/updateManualDistribution.do'
        data={"warehouseCode":self.warehouseCode,
              "month":"",
              "storehouseCode": "",
              "logisticOrderId":order_no}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        if re_json["message"] == "SUCCESS":
            print("库存分配成功")
            time.sleep(10)
        else:
            print("库存分配失败" + re_result.text)

    def doSearchWaveNo(self):
        #查询未释放波次
        startCreateDate = time.strftime("%Y-%m-%d", time.localtime(time.time() - 604800)) + " 00:00:00"
        endCreateDate = time.strftime("%Y-%m-%d", time.localtime()) + " 23:59:59"
        url='http://jwmspre.cnsuning.com/jwms-web/out/outWaveManage/doSearch.do'
        data={"warehouseId":self.warehouseCode,
              "status":"01",
              "startCreateDate": startCreateDate,
              "endCreateDate":endCreateDate,
              "draw":"17",
              "start":"0",
              "page":"1",
              "rows":"10"}
        re_result=self.session.post(url=url,data=data,headers=self.headers)
        re_json=json.loads(re_result.text)
        waveNo = ""
        if re_json["result"]==True:
            if re_json["data"]["datas"]:
                waveNo = re_json["data"]["datas"][0]["waveNo"]
                print("有未释放波次:" + str(waveNo))
            else:
                print("没有未释放波次")
        else:
            print("查询未释放波次失败:" + re_result.text)
        return waveNo

    def searchWellen(self):
        #统计波次
        url='http://jwmspre.cnsuning.com/jwms-web/out/manualCreateWave/doSearchCount.do'
        data={"warehouseId":self.warehouseCode,
              "logisticOrderId":self.OMSITEM,
              "receiptState":"00",
              "logisticsMethod": "00",
              "reachPayment": "00",
              "draw": "3",
              "start": "0",
              "page": "1",
              "rows": "10"}

        cut=0
        while cut!=180:
            re_result = self.session.post(url=url, data=data, headers=self.headers)
            re_json = json.loads(re_result.text)
            if re_json["express"] == 1:
                print("统计波次成功")
                break
            elif re_json["express"] == 0:
                print("未查询到统计波次，请稍等" + str(cut))
                time.sleep(5)
                cut = cut + 5
            else:
                print("统计波次失败" + re_result.text)
                break



    def getWellen(self):
        #获取波次
        url='http://jwmspre.cnsuning.com/jwms-web/out/manualCreateWave/doManualCreateWave.do'
        data = {"warehouseId": self.warehouseCode,
                "logisticOrderId": self.OMSITEM,
                "receiptState": "00",
                "logisticsMethod": "00",
                "reachPayment": "00",
                "draw": "3",
                "start": "0",
                "page": "1",
                "rows": "10"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            waveNo = re_json["waveNoList"][0]
            print("获取波次号:" + str(waveNo))
            return str(waveNo)
        else:
            print("获取波次失败:"+re_result.text)

    def createWellen(self,waveNoList=''):
        #创建波次
        url='http://jwmspre.cnsuning.com/jwms-web/out/manualCreateWave/sumTable.do'
        data={"warehouseCode":self.warehouseCode,
              "waveNoList":waveNoList}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["data"]["datas"]["datas"][0]["waveType"]=="销售出库":
            print("创建波次成功")
        else:
            print("创建波次失败：" + re_result.text)

    def releaseWellen(self,waveNoList=''):
        #释放波次
        url='http://jwmspre.cnsuning.com/jwms-web/out/outWaveManage/releaseWaves.do'
        data={"chooseWarehouseCode":self.warehouseCode,
              "chooseContextArr":waveNoList}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"] == True:
            print("释放波次成功"+ re_result.text)
        else:
            print("释放波次失败：" + re_result.text)


    def pickPrint(self,pickNo=''):
        #打印拣选单
        url='http://jwmspre.cnsuning.com/jwms-web/out/pickingOrder/pickPrint.do'
        data={"warehouseCode":self.warehouseCode,
              "pickNo":pickNo,
              "printFlag":"3"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            print("打印拣选单成功")
        else:
            print("打印拣选单失败" + re_result.text)


    def pickLogin(self,pickNo=''):
        #登陆包装复核
        url='http://jwmspre.cnsuning.com/jwms-web/out/packCheck/pickLogin.do'
        data={"workCode":"bz123",
              "pickConCode":pickNo,
              "reConCode":"3CFY-006-0101"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        # print("登陆包装复核：" + re_result.text)
        re_json = json.loads(re_result.text)
        if re_json["pickingOrders"][0]["pickNo"]==pickNo:
            print("登陆包装复核成功")
        else:
            print("登陆包装复核失败" + re_result.text)


    def getPackageInfo(self,scanCode='',pickNo=''):
        #校验商品信息
        url='http://jwmspre.cnsuning.com/jwms-web/out/universalPackCheck/getPackageInfoBySku.do'
        data={"warehouseCode":self.warehouseCode,
              "pickNo":pickNo,
              "scanCode":scanCode}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["message"]=="校验通过":
            print("商品信息校验成功")
            time.sleep(2)
        else:
            print("商品信息校验失败" + re_result.text)

    def saveCheckSku(self,pickNo='',packageNo='',skuCode='',logisticOrderId=''):
        #输入包材
        url='http://jwmspre.cnsuning.com/jwms-web/out/packCheck/saveCheckSku.do'
        data={"warehouseCode":self.warehouseCode,
              "containerCode":"3CFY-006-0101",
              "pickContainer":"null",
              "workbenchCode":"bz123",
              "pickNo":pickNo,
              "packageNo":packageNo,
              "logisticOrderId":logisticOrderId,
              "skuCode":skuCode,
              "checkSkuNum":"1",
              "materialsCode":"GKBZ"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"] == True:
            print("包装复核成功")
        else:
            print("包装复核失败：" + re_result.text)

    def queryReportPage(self):
        #通过订单号查询拣选单号
        url='http://jwmspre.cnsuning.com/jwms-web/report/pickDetail/queryReportPage.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM,
              "offset":"0",
              "limit":"10"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            pickNo = re_json["data"]["datas"][0]["pickNo"]
            print("获取拣选单号：" + str(pickNo))
            return pickNo
        else:
            print("获取拣选单号失败：" + re_result.text)

    def findPackageSumInfo(self,pickNo=''):
        #获取复核商品信息
        url='http://jwmspre.cnsuning.com/jwms-web/out/packCheck/findPackageSumInfo.do'
        data={"warehouseCode":self.warehouseCode,
              "pickNo":pickNo}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            print("获取复核商品信息成功")
            return re_json
        else:
            print("获取复核商品信息失败：" + re_result.text)


    def searchSkuCode(self,sncmmdtyCode=''):
        #查询商品条码
        url='http://jwmspre.cnsuning.com/jwms-web/base/newCmmdtyCollect/search.do'
        data={"sncmmdtyCode":sncmmdtyCode}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            SkuCode = re_json["data"]["datas"][0]["barCode"]
            print("获取商品条码成功：" + str(SkuCode))
            return SkuCode
        else:
            print("获取商品条码失败：" + re_result.text)


    def queryOutPackage(self):
        #查询包裹号
        url='http://jwmspre.cnsuning.com/jwms-web/out/outPackage/queryOutPackage.do'
        data={"warehouseCode":self.warehouseCode,
              "logisticOrderId":self.OMSITEM}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["result"]==True:
            expressCode = re_json["data"][0]["expressCode"]
            print("包裹号：" + str(expressCode))
            return expressCode
        else:
            print("查询包裹号失败：" + re_result.text)

class SendGoods(FuncBase):
    def assigne(self,order_no=''):
        # 库存分配
        while 1:
            RepertoryDetil = self.queryOrderRepertory(order_no=order_no)  # 查询库存分配详情
            if RepertoryDetil["data"]["datas"]:
                if RepertoryDetil["data"]["datas"][0]["repertoryStatusDesc"]=="未分配":
                    self.assignedOrder(order_no=order_no)  ##库存分配

                    time.sleep(10)
                else:
                    break
            else:
                break

    def wellen(self):
        #创建波次

        waveNo = self.doSearchWaveNo()          #查询是否有未释放波次
        if waveNo=="":
            pass
        else:
            waveNoList = '["'+ str(waveNo) +'"]'    ##组装波次序列
            self.releaseWellen(waveNoList=waveNoList)  ##释放波次
        self.searchWellen()              ##统计波次
        waveNo = self.getWellen()        ##获取波次

        waveNoList = '["'+ str(waveNo) +'"]'       ##组装波次序列
        self.createWellen(waveNoList=waveNoList)   ##创建波次
        self.releaseWellen(waveNoList=waveNoList)  ##释放波次

    def printPick(self):
        pickNo = self.queryReportPage()  ##获取拣选单号
        self.pickPrint(pickNo=pickNo)         ##打印拣选单

    def packaging(self):
        #包装复核
        pickNo = self.queryReportPage()  ##获取拣选单号
        self.pickLogin(pickNo=pickNo)  ##登陆包装复核
        SkuInfo = self.findPackageSumInfo(pickNo=pickNo)  # 获取复核商品信息
        for skuinfo in SkuInfo["data"]["packageList"][0]["skuList"]:
            packageNo = skuinfo["package_no"]
            skuCode = skuinfo["sku_code"]   #商品编码
            logisticOrderId = skuinfo["logistic_order_id"]   #oms订单行号
            scanCode = self.searchSkuCode(sncmmdtyCode=skuCode)  ##查询商品条码
            for i in range(int(skuinfo["amount"]) - int(skuinfo["pick_num"])):
                self.getPackageInfo(scanCode=scanCode, pickNo=pickNo)  ##校验商品信息
                self.saveCheckSku(pickNo=pickNo, packageNo=packageNo, skuCode=skuCode,
                                  logisticOrderId=logisticOrderId)  ##输入包材，包装复核

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
        data={"goodsType":"0",
              "scanType":"03",
              "lastSiteId": "L025",
              "factory": "L025",
              "wayBillNo": expressCode,
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
                    time.sleep(5)
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

    def scanPackageWoi(self,packageNo=''):
        #获取包裹信息
        url='http://edspre.cnsuning.com/eds-web/deliveryoffstation/profile/scanPackageWoi.action'
        data={"packageNo":packageNo,
              "checkBol":"flase"}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["data"][0]["BGH"]==packageNo:
            print("获取包裹信息成功")
        else:
            print("获取包裹信息失败：" + re_result.text)

    def doOffStationWoi(self,userId=''):
        #配送离站
        url='http://edspre.cnsuning.com/eds-web/deliveryoffstation/profile/doOffStationWoi.action'
        data={"dnos":self.OMSITEM,
              "userId":userId,
              "operator": self.user}
        re_result = self.session.post(url=url, data=data, headers=self.headers)
        re_json = json.loads(re_result.text)
        if re_json["returnCode"]=="S":
            shpmntno = re_json["list"]["zylist"]  # 装运编号
            print("配送离站成功")
            time.sleep(5)
            return shpmntno
        else:
            print("配送离站失败：" + re_result.text)

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
    def send(self,omsOrderNo,operateType):

        sendOMS = OmsdBack(omsOrderNo=omsOrderNo)
        sendOMS.creatOrdiDeli()  # 生成发货指令

        OMSITEM = "OMS" + omsOrderNo + "01"
        data_init = FuncBase(OMSITEM=OMSITEM)
        send = SendGoods(OMSITEM=OMSITEM)
        Assigned_info = data_init.queryAssigned()  # 查询订单状态
        bolCode = Assigned_info[1]   #合单号
        orderNo_dict = data_init.queryBolCode(bolCode=bolCode)   #合并的订单
        if orderNo_dict!={}:
            for i in orderNo_dict.items():
                order_no = i[0]
                order_status = i[1]
                if order_status == "待分配":
                    send.assigne(order_no=order_no)  # 分配
                    Assigned_info = data_init.queryAssigned()  # 查询订单状态
        else:
            order_status = Assigned_info[0]
            if order_status == "待分配":
                send.assigne(order_no=OMSITEM)  # 分配
                Assigned_info = data_init.queryAssigned()  # 查询订单状态

        order_status = Assigned_info[0]
        print("当前订单状态:" + str(order_status))

        if order_status == "分配成功":
            send.wellen()  # 创建波次
            send.printPick()  # 打印拣选单
            send.packaging()  # 包装复核

        elif order_status == "拣选单创建成功":
            send.printPick()  # 打印拣选单
            send.packaging()  # 包装复核

        elif order_status == "已拣选":
            send.packaging()  # 包装复核

        outtime = 0  # 初始化超时时间
        while outtime != 600:
            Assigned_info = data_init.queryAssigned()  # 查询订单状态
            order_status = Assigned_info[0]
            print("当前订单状态:" + str(order_status) + str(outtime))
            if order_status == "已发运":
                expressCode = data_init.queryOutPackage()  ##查询包裹号
                logistic = Logistic(OMSITEM=OMSITEM)
                logistic.daoJian(expressCode=expressCode)  # 到件
                Driver = logistic.queryStationDriver()  # 获取配送员
                logistic.scanPackageWoi(packageNo=expressCode)  # 获取包裹信息
                shpmntno = logistic.doOffStationWoi(userId=Driver)  # 配送离站
                logistic.saveBillcancel(shpmntno=shpmntno, expressCode=expressCode, operateType=operateType)  ##销单
                break
            elif order_status != "已复核":
                if order_status != "已拣选":
                    break
            time.sleep(10)
            outtime = outtime + 10

if __name__ == '__main__':

    omsOrderNo='00105640312301'

    operateType = "access"  ##妥投-access    拒收-reject

    sendGoodsjob().send(omsOrderNo,operateType)