#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: Base.py
@time: 2019-05-09 11:44:57
@desc:标准api接口
'''

from API.D0001_STANDAPI.url import StandConfig
import time
from Tools.tools import MySql
from Tools.tools import Common
import json
from decimal import Decimal
import random
from Tools.url_code import url



class StandApi():
    def __init__(self,envi,appKey,appSecret,isLog):
        self.mysql = MySql(envi)
        self.appKey = appKey
        self.appSecret=appSecret
        self.common=Common(envi=envi)
        self.host = self.common.scHost_bz()
        self.GetSign = self.common.getSign
        self.nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.reqData = StandConfig.datas
        self.timestmp = int((time.time())*1000)
        self.isLog = isLog


    def getCategory(self):
        """获取商品目录接口"""
        FuncName = self.getCategory.__doc__

        data = StandConfig.GetCategory.data
        appMethod = StandConfig.GetCategory.method

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def productSearch(self,searchContent='',cityCode='025',categoryIdOne='',categoryIdTwo='',categoryIdThree='', \
                      min='',max='',sortType='0',page='1',limit='200',aggregate='0',attrList='',brandId=''):
        """政企商品搜索接口"""
        # :param searchContent	String	N	惠普打印机	搜索关键字
        # :param cityCode	String	Y	025	城市编码
        # :param categoryIdOne	String	N	1111	一级类目
        # :param categoryIdTwo	String	N	11	    二级类目
        # :param categoryIdThree	String	N	11	    三级类目
        # :param min	String	N	100	最低价格
        # :param max	String	N	200	最高价格
        # :param sortType	String	N	1	排序方式0默认排序1销量 2价格升 3价格降
        # :param page	String	N	1	页码
        # :param limit	String	N	200	分页条数
        #
        # :param aggregate	String	N	1	    [高级搜索]是否获取高级搜索条件0否1是
        # :param attrList	   String	N	111	    [高级搜索]属性列表
        # :param brandId	   String	N	0IAC	[高级搜索]品牌编码
        FuncName = self.productSearch.__doc__

        data = StandConfig.ProductSearch.data
        appMethod = StandConfig.ProductSearch.method

        data = data % ({"searchContent": searchContent, "cityCode": cityCode, "categoryIdOne": categoryIdOne, \
                        "categoryIdTwo": categoryIdTwo, "categoryIdThree": categoryIdThree, "min": min, "max": max, \
                        "sortType": sortType, "page": page, "limit": limit, "aggregate": aggregate,
                        "attrList": attrList, "brandId": brandId})


        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def categorySearch(self,keyword=''):
        """商品类目搜索"""
        FuncName = self.categorySearch.__doc__

        data = StandConfig.CategorySearch.data
        appMethod = StandConfig.CategorySearch.method

        data = data % ({"keyword": keyword})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def productMapping(self,currentPage='1'):
        """查询商品映射关系"""
        #currentPage   页码
        FuncName = self.productMapping.__doc__

        data = StandConfig.ProductMapping.data
        appMethod = StandConfig.ProductMapping.method

        data = data % ({"currentPage": currentPage})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getProductCluster(self,skuId='121347748'):
        """查询商品映射关系"""
        # :param :characterName	String	颜色	特征展示名称
        # :param :characterValueId	String	20017	特征值ID
        # :param :characterValueName	String	黑色	特征值名称
        # :param :imageShowFlag	String	0	是否展示图片(0：不展示；1：展示)
        FuncName = self.getProductCluster.__doc__

        data = StandConfig.GetProductCluster.data
        appMethod = StandConfig.GetProductCluster.method

        data = data % ({"skuId": skuId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def judgeFacProduct(self,skuIds,cityId):
        """判断商品是否厂送接口"""
        # :param :isFactorySend	01：是厂送 02：不是厂送

        FuncName = self.judgeFacProduct.__doc__

        data = StandConfig.JudgeFacProduct.data
        appMethod = StandConfig.JudgeFacProduct.method

        skulist=""

        for skuId in skuIds.split(","):
            skulist = skulist + f"<skuIds><skuId>{skuId}</skuId></skuIds>"

        data = data % ({"skuIds": skulist, "cityId": cityId})


        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]

        print(redata)
        try:
            tmp = json.loads(redata)
            for sku in tmp["sn_responseContent"]["sn_body"]["getJudgefacproduct"]["results"]:
                if sku["isFactorySend"]==str("02"):
                    print(str(sku)+"   自营品")
                elif sku["isFactorySend"]==str("01"):
                    print(str(sku)+"   厂送品")
        except:
            print(tmp)

        return redata

    def searchProdExtend(self,skuId='121347748'):
        """查询商品扩展信息"""
        # :param increaseTicket: String	01/02	是否支持开增票(01-支持；02-不支持)
        # :param noReasonLimit: String	7	支持无理由退货的天数
        # :param noReasonTip: String	7天无理由退货	退货描述
        # :param returnGoods: String	01/02	是否支持无理由退货(01-7天无理由退货；02-不支持退货)
        FuncName = self.searchProdExtend.__doc__

        data = StandConfig.SearchProdExtend.data
        appMethod = StandConfig.SearchProdExtend.method

        data = data % ({"skuId":skuId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def queryProdExtend(self,skuId='121347748',cityId='025'):
        """查询商品扩展信息（新）"""
        # :param increaseTicket: String	01/02	是否支持开增票(01-支持；02-不支持)
        # :param noReasonLimit: String	7	支持无理由退货的天数
        # :param noReasonTip: String	7天无理由退货	退货描述
        # :param returnGoods: String	01/02	是否支持无理由退货(01-7天无理由退货；02-不支持退货)
        FuncName = self.queryProdExtend.__doc__

        data = StandConfig.QueryProdExtend.data
        appMethod = StandConfig.QueryProdExtend.method

        data = data % ({"skuId":skuId,"cityId":cityId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getSpecialGoods(self,categoryId=''):
        """获取特殊商品池"""
        # generalSku     通码，具有相同通码的sku表示一组类似的商品
        # cmmdtyType     商品类型 3：实体储值卡 4：电子储值卡5：实体提货卡 6：电子提货卡 7：普通服务商品
        FuncName = self.getSpecialGoods.__doc__

        data = StandConfig.GetSpecialGoods.data
        appMethod = StandConfig.GetSpecialGoods.method

        data = data % ({"categoryId":categoryId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getPool(self,categoryId='',pgSize='100',pageNum='1'):
        """获取商品池商品"""
        # generalSku     通码，具有相同通码的sku表示一组类似的商品
        # cmmdtyType     商品类型   1：普通商品   2：套餐商品
        FuncName = self.getPool.__doc__

        data = StandConfig.GetPool.data
        appMethod = StandConfig.GetPool.method

        data = data % ({"pgSize":pgSize,"pageNum":pageNum,"categoryId":categoryId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getPictureDetail(self,skuId=''):
        """获取商品详情接口"""

        FuncName = self.getPictureDetail.__doc__

        data = StandConfig.GetPictureDetail.data
        appMethod = StandConfig.GetPictureDetail.method

        data = data % ({"skuId":skuId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getPicture(self,skuId=''):
        """获取商品图片接口"""
        # primary： 是否为主图   1：是   0：否

        FuncName = self.getPicture.__doc__

        data = StandConfig.GetPicture.data
        appMethod = StandConfig.GetPicture.method
        sku=""

        for i in skuId.split(","):
            sku = sku + ("<skuIds><skuId>%s</skuId></skuIds>" % i)
        data = data % ({"skuIds": sku})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def batchStatus(self,skuIds='',cityId='025',isCmbc='N'):
        """商品上下架状态查询接口"""
        # state		上下架状态  1：在售   0：下架
        # isCmbc    招商用户表示，为Y时，cityId必填

        FuncName = self.batchStatus.__doc__

        data = StandConfig.BatchStatus.data
        appMethod = StandConfig.BatchStatus.method
        skulist=""

        for skuId in skuIds.split(","):
            skulist = skulist + f"<skuIds><skuId>{skuId}</skuId></skuIds>"
        if isCmbc=='Y':
            skulist = skulist + "<cityId>{cityId}</cityId>"
        data = data % ({"skuIds":skulist})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        try:
            tmp = json.loads(redata)
            skuList=tmp["sn_responseContent"]["sn_body"]["getBatchProdSaleStatus"]["onShelvesList"]
            for sku in skuList:
                if sku["state"]=="1":
                    print("商品编号：" + sku["skuId"] + ",在售")
                elif sku["state"]=="0":
                    print("商品编号：" + sku["skuId"] + ",下架")
        except Exception:
            pass

        return redata

    def prodReview(self,skuIds=''):
        """获取商品评价接口"""
        # generalRate       中评率
        # goodRate          好评率
        # poorRate          差评率

        FuncName = self.prodReview.__doc__

        data = StandConfig.ProdReview.data
        appMethod = StandConfig.ProdReview.method
        skulist=""

        for skuId in skuIds.split(","):
            skulist = skulist + f"<skuIds><skuId>{skuId}</skuId></skuIds>"


        data = data % ({"skuId":skulist})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        # print(redata)

        try:
            tmp = json.loads(redata)
            skuList = tmp["sn_responseContent"]["sn_body"]["queryProdReview"]["resultInfo"]
            for sku in skuList:
                print("商品编码：" + sku["skuId"])
                print("好评率：" + sku["goodRate"])
                print("中评率：" + sku["generalRate"])
                print("差评率：" + sku["poorRate"])
        except Exception:
            pass

        return redata

    def combinationProd(self,skuId=''):
        """获取套餐清单"""

        FuncName = self.combinationProd.__doc__

        data = StandConfig.CombinationProd.data
        appMethod = StandConfig.CombinationProd.method


        data = data % ({"skuId":skuId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getPrice(self,skuIds='',city=''):
        """查询价格接口"""
        # price           价格
        # snPrice         易购价
        # discountRate    折扣率
        # tax             税率
        # taxprice        税额
        # nakedprice      裸价

        FuncName = self.getPrice.__doc__

        data = StandConfig.GetPrice.data
        appMethod = StandConfig.GetPrice.method
        skulist = ""

        for sku in skuIds.split(','):
            skulist = skulist + f"<skus><skuId>{sku}</skuId></skus>"
        data = data % ({"skus":skulist,"city":city})
        # print(data)
        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        try:
            skuPrice = {}
            tmp = json.loads(redata)
            for sku in tmp["sn_responseContent"]["sn_body"]["queryPrice"]["skus"]:
                skuPrice.update({sku["skuId"]:sku["price"]})
        except:
            print(tmp)
        print('价格：'+str(skuPrice))

        return skuPrice

    def getInventory(self,skuIds='',city='',countyId='',num=''):
        """精准库存查询接口"""
        # 库存状态   00：有货   01：暂不销售   02：无货   03：库存不足

        FuncName = self.getInventory.__doc__

        data = StandConfig.GetInventory.data
        appMethod = StandConfig.GetInventory.method
        skulist=""

        for skuId in skuIds.split(","):
            skulist = skulist + f"<skuIds><num>{num}</num><skuId>{skuId}</skuId></skuIds>"

        data = data % ({"skuIds": skulist, "city": city, "countyId":countyId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        try:
            tmp = json.loads(redata)
            for sku in tmp["sn_responseContent"]["sn_body"]["getInventory"]["resultInfo"]:
                if sku["state"]=="00":
                    print({sku["skuId"]: sku["state"]+",有货"})
                elif sku["state"]=="01":
                    print({sku["skuId"]: sku["state"]+"暂不销售"})
                elif sku["state"] == "02":
                    print({sku["skuId"]: sku["state"]+",无货"})
                elif sku["state"] == "03":
                    print({sku["skuId"]: sku["state"]+",库存不足"})
        except Exception:
            raise resp


        return redata

    def getStock(self,skuIds='',city=''):
        """批量查询库存接口"""
        # 库存状态   0：现货     1：在途      2：无货

        FuncName = self.getStock.__doc__

        data = StandConfig.GetStock.data
        appMethod = StandConfig.GetStock.method
        skulist=""

        for skuId in skuIds.split(","):
            skulist = skulist+ f"<skuIds><skuId>{skuId}</skuId></skuIds>"
        data= data %({"skus":skulist,"cityId":city})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        try:
            tmp = json.loads(redata)
            for sku in tmp["sn_responseContent"]["sn_body"]["queryMpStock"]["resultInfo"]:
                if sku["state"] == 0:
                    print({sku["skuId"]: str(sku["state"]) + ",现货"})
                elif sku["state"] == 1:
                    print({sku["skuId"]: str(sku["state"]) + ",在途"})
                elif sku["state"] == 2:
                    print({sku["skuId"]: str(sku["state"]) + ",无货"})

        except Exception:
            raise resp

        return redata

    def addOrder(self,skuIds,companyCustNo="",nums='1',orderType=0,invoiceState=1,payType="08",invoiceType=1,\
                       province="100",city="025",county="01",townId='99',address='一九一二',isservFee='Y'):
        """老创建订单接口"""
        #说明：下多个品时，skuIds="121347748,121347746",nums="1,2"
        #则121347748购买1个，121347746购买2个

        # companyCustNo: 子账号会员编码
        # orderType: 订单类型(0.实时型订单1.预占型订单)
        # invoiceState: 是否开发票(1 = 开，0 = 不开)
        # payType: 支付方式(01 - 在线支付；03 - 货到付款现金；04 - 货到付款POS；09 - 预付款；08 - 账期)
        # invoiceType: 发票类型：1 = 增票（不指定公司开票）       6 = 增票 （指定公司开票）
        #                       4 = 电子发票（不指定公司开票）   9 = 电子发票（指定公司开票）
        #                       2 = 普通发票（卷票，票随货走，不指定公司开票）

        FuncName = self.addOrder.__doc__

        tradeNo = "order" + str(self.timestmp) + str(random.randint(1,100))
        data = StandConfig.AddOrder.data
        appMethod = StandConfig.AddOrder.method
        skuInfo = ""
        amount = 0
        servFee = 0
        i = 0
        sku = skuIds.split(",")

        for num in nums.split(','):
            priceInfo = self.getPrice(sku[i],city)
            price = list(priceInfo.values())[0]
            skuInfo = skuInfo + "<sku><num>%(num)s</num><skuId>%(sku)s</skuId>\
                <unitPrice>%(price)s</unitPrice></sku>" % ({"num": num, "sku": sku[i], "price": price})
            val = float(price) * int(num)
            amount = float('%.2f' % Decimal(amount)) + float('%.2f' % Decimal(val))
            amount = float('%.2f' % amount)
            i = i + 1
        # print(skuInfo)

        if isservFee=='Y':
            if amount < 86:
                servFee = 5
        data = data % ({"province":province,"city":city,"county":county,"townId":townId,"address":address + tradeNo,"payTpye":payType,"orderType":orderType,
                        "invoiceState":invoiceState,"invoiceType":invoiceType,"tradeNo":tradeNo,"companyCustNo":companyCustNo,
                        "servFee":servFee,"amount":float('%.2f' % Decimal(amount)),"skuInfo":skuInfo})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata


    def cancleOrder(self,orderId=''):
        """取消预占库存订单接口"""

        FuncName = self.cancleOrder.__doc__

        data = StandConfig.CancleOrder.data
        appMethod = StandConfig.CancleOrder.method

        data = data % ({"orderId": orderId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def addMixOrder(self,skuIds,companyCustNo="",nums='1',orderType=0,hopeArrivalTime='',\
                        isInvoice=1,payType="01",invoiceType=4,\
                    province="100",city="025",county="01",townId='99',address='南京玄武1',isservFee='N'):
        """新创建订单接口"""
        #说明：下多个品时，skuIds="121347748,121347746",nums="1,2"
        #则121347748购买1个，121347746购买2个

        # companyCustNo: 子账号会员编码
        # orderType: 订单类型(0.实时型订单1.预占型订单)
        # isInvoice: 是否开发票(1 = 开，0 = 不开)
        # payType: 支付方式(01-在线支付-易付宝；03-货到付款现金；04-货到付款POS；05-支付宝支付；08-账期；
        #                  09-预付款；11-第三方支付;12-企业汇款支付;020-在线支付-网银)
        # invoiceType: 发票类型：1-增值税专票;2-普票（即卷票，票随货走）;
        #                       3-增值税普票（即平推式普票，票货分离）；4-电子发票

        FuncName = self.addMixOrder.__doc__

        tradeNo = "mix" + str(self.timestmp) + str(random.randint(1,1000))
        data = StandConfig.AddMixOrder.data
        appMethod = StandConfig.AddMixOrder.method
        skuInfo = ""
        amount = 0
        servFee = 0
        i=0
        sku = skuIds.split(",")

        for num in nums.split(','):
            priceInfo = self.getPrice(sku[i],city)
            price = list(priceInfo.values())[0]
            skuInfo = skuInfo + "<sku><num>%(num)s</num><skuId>%(sku)s</skuId>\
                <unitPrice>%(price)s</unitPrice></sku>" % ({"num": num, "sku": sku[i], "price": price})
            val = float(price) * int(num)
            amount = float('%.2f' % Decimal(amount)) + float('%.2f' % Decimal(val))
            amount = float('%.2f' %amount)
            i = i + 1

        if isservFee == 'Y':
            if amount < 86:
                servFee = 5

        pay7207 = round(Decimal(str(amount)) / Decimal(3),2)
        pay7208 = round(Decimal(str(amount)) / Decimal(3),2)
        pay7209 = float(Decimal(str(amount)) - (Decimal(str(pay7207))+Decimal(str(pay7208))))

        data = data % (
        {"province": province, "city": city, "county": county, "townId":townId,"address":address + tradeNo,"payTpye": payType, "orderType": orderType,
         "isInvoice": isInvoice, "invoiceType": invoiceType, "tradeNo": tradeNo, "companyCustNo": companyCustNo,"hopeArrivalTime":hopeArrivalTime,
         "servFee": servFee, "amount": float('%.2f' % Decimal(amount)), "skuInfo": skuInfo,"7207":pay7207,"7208":pay7208,"7209":pay7209})
        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def mixPayOrder(self,orderId=''):
        """混合支付确认预占接口"""

        FuncName = self.mixPayOrder.__doc__

        data = StandConfig.MixPayOrder.data
        appMethod = StandConfig.MixPayOrder.method
        payInfo = ""
        payBrach = self.mysql.searchs("select branch_pay_way,payment_amount from srcorder_sub_paymethod where gc_order_no='%s'" % orderId)

        for i in payBrach:
            payInfo = payInfo + ("<subPaymentModes>\
            <payAmount>%(amount)s</payAmount><payCode>%(payCode)s</payCode></subPaymentModes>" %({"payCode":i[0],"amount":i[1]}))

        data = data % ({"payInfo":payInfo,"orderId":orderId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def unPaidOrder(self,orderId=''):
        """未支付订单取消接口"""

        FuncName = self.unPaidOrder.__doc__

        data = StandConfig.UnPaidOrder.data
        appMethod = StandConfig.UnPaidOrder.method

        data = data % ({"orderId":orderId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def cancleOrderEnd(self,skuId='',orderId='',reason='0101',reasonDetails='不想要了',\
                       bankName='03',cardUsername='王大力',cardNumber='6200121394857114'):
        """退货申请接口"""
        #skuId支持输入多个，以逗号分隔


        # reason      商品编码为厂送商品时必填
        #             0301：无理由退货
        #             0101：商品破损
        #             0102：成套商品部分少发
        #             0103：商品质量问题
        #             0105：商品过期 / 接近有效期
        #             0106：商品名称一致，但与网页介绍不符
        #             0201：未按约定时间上门
        #             0202：服务态度差
        #             0203：商品发错
        #             0204：对收费价格不满
        #             0205：安装 / 维修技能差
        #             0401：价格波动
        # reasonDetails    退货详细原因厂送商品退货时需要，非必填
        # cardNumber     银行卡号,支付方式货到付款现金时必填
        # bankName       支付方式货到付款现金时必填
        #                 01 - 中国银行
        #                 02 - 工商银行
        #                 03 - 建设银行
        #                 04 - 交通银行
        #                 05 - 华夏银行
        #                 06 - 招商银行
        #                 07 - 光大银行
        #                 08 - 农业银行
        #                 09 - 民生银行
        #                 10 - 兴业银行
        #                 12 - 北京银行
        #                 13 - 浦发银行
        #                 14 - 上海银行
        #                 15 - 平安银行
        #                 16 - 邮政储蓄银行
        # cardUsername     持卡人姓名,支付方式货到付款现金时必填


        FuncName = self.cancleOrderEnd.__doc__

        data = StandConfig.CancleOrderEnd.data
        appMethod = StandConfig.CancleOrderEnd.method

        skus=""
        for i in skuId.split(","):
            skus = skus + "<skus><skuId>{}</skuId><reason>{}</reason><reasonDetails>{}</reasonDetails></skus>".format(i,reason,reasonDetails)

        data = data % ({"skus": skus,"orderId":orderId,"reason":reason,"reasonDetails":reasonDetails,\
                        "bankName":bankName,"cardUsername":cardUsername,"cardNumber":cardNumber})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def returnPartOrder(self,skuId='',num='',orderId='',reason='',reasonDetails='',\
                       bankName='',cardUsername='',cardNumber='',provinceId='',cityId='',countyId='',townId='',address='',aftersaleName='',aftersalePhone=''):
        """部分退货接口"""
        #说明：支持退多个品，如skuId='121347748,121347746',num='1,2'
        #则121347748退1个，121347746退2个

        # reason      商品编码为厂送商品时必填
        #             0301：无理由退货
        #             0101：商品破损
        #             0102：成套商品部分少发
        #             0103：商品质量问题
        #             0105：商品过期 / 接近有效期
        #             0106：商品名称一致，但与网页介绍不符
        #             0201：未按约定时间上门
        #             0202：服务态度差
        #             0203：商品发错
        #             0204：对收费价格不满
        #             0205：安装 / 维修技能差
        #             0401：价格波动
        # reasonDetails    退货详细原因厂送商品退货时需要，非必填
        # cardNumber     银行卡号,支付方式货到付款现金时必填
        # bankName       支付方式货到付款现金时必填
        #                 01 - 中国银行
        #                 02 - 工商银行
        #                 03 - 建设银行
        #                 04 - 交通银行
        #                 05 - 华夏银行
        #                 06 - 招商银行
        #                 07 - 光大银行
        #                 08 - 农业银行
        #                 09 - 民生银行
        #                 10 - 兴业银行
        #                 12 - 北京银行
        #                 13 - 浦发银行
        #                 14 - 上海银行
        #                 15 - 平安银行
        #                 16 - 邮政储蓄银行
        # cardUsername     持卡人姓名,支付方式货到付款现金时必填

        FuncName = self.returnPartOrder.__doc__

        data = StandConfig.ReturnPartOrder.data
        appMethod = StandConfig.ReturnPartOrder.method

        skuIdList=skuId.split(",")
        numList=num.split(",")

        skuinfo = ""
        i = 0
        for k in skuIdList:
            skuinfo = skuinfo + "<skus><skuId>{}</skuId><num>{}</num><reason>{}</reason>\
            <reasonDetails>{}</reasonDetails></skus>".format(skuIdList[i],numList[i],reason,reasonDetails)
            i = i + 1

        data = data % ({"skuIdinfo":skuinfo,"orderId":orderId,"bankName":bankName,"cardUsername":cardUsername,\
                        "cardNumber":cardNumber,"provinceId":provinceId,"cityId":cityId,"countyId":countyId,\
                        "townId":townId,"address":address,"aftersaleName":aftersaleName,"aftersalePhone":aftersalePhone})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getStatus(self,orderId=''):
        """获取订单状态接口"""
        # 订单状态   1: 审核中;2: 待发货;3: 待收货;4: 已完成;5: 已取消;6: 已退货;\
        #           7: 待处理;8：审核不通过，订单已取消;9：待支付

        FuncName = self.getStatus.__doc__

        data = StandConfig.GetStatus.data
        appMethod = StandConfig.GetStatus.method

        data = data % ({"orderId":orderId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def orderDetail(self,orderId=''):
        """查询单个订单详细"""

        FuncName = self.orderDetail.__doc__

        data = StandConfig.OrderDetail.data
        appMethod = StandConfig.OrderDetail.method

        data = data % ({"orderId":orderId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def queryItemDetail(self,orderItem=''):
        """批量查询订单行接口"""

        FuncName = self.queryItemDetail.__doc__

        data = StandConfig.QueryItemDetail.data
        appMethod = StandConfig.QueryItemDetail.method
        orderIds=""

        for i in orderItem.split(","):
            orderIds = orderIds + ("<orderItemIds><orderItemId>%s</orderItemId></orderItemIds>" % i)
        data = data % ({"orderIds":orderIds})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def queryOrderAccount(self,startDate,endDate,pageNo="1",pageSize="50",orderStatus="0"):
        """订单对账接口"""
        # :param startDate	String	Y	2015-10-20	开始时间（yyyy-MM-dd）
        # :param endDate	String	Y	2015-11-20	结束时间（yyyy-MM-dd 与开始时间相差不超过1个月）
        # :param orderStatus	String	Y	0	订单状态 0：所有状态 1:待审核 2:待支付 3:待收货 4:已完成 5:已取消 6:已退货 7：审核不通过
        # :param pageNo	String	N	2	当前页码 表示取第几页
        # :param pageSize	String	N	20	每页条数

        FuncName = self.queryOrderAccount.__doc__

        data = StandConfig.QueryOrderAccount.data
        appMethod = StandConfig.QueryOrderAccount.method

        data = data % ({"startDate":startDate,"endDate":endDate,"pageNo":pageNo,"pageSize":pageSize,"orderStatus":orderStatus})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def queryOrderItem(self,startDate,endDate,orderItemStatus="2",dateType='1',companyCusNo='',pageLen='50',pageNum="1"):
        """订单行对账接口"""
        # :param startDate	String	Y	2015-10-20	开始时间（yyyy-MM-dd）
        # :param endDate	String	Y	2015-11-20	结束时间（yyyy-MM-dd 与开始时间相差不超过1个月）
        # :param orderItemStatus	String	Y	0	订单行状态： 1:审核中; 3:待收货或待服务; 4:已完成或服务完成; 5:已取消; 6:已退货; 7:待处理; 8:审核不通过，订单已取消; 9:待支付;
        # :param dateType String	Y	0	时间类型：0：订单行状态更新时间，1：订单行创建时间
        # :param pageNum	String	Y	1	页码，默认传1
        # :param companyCusNo String	N	6114631093	企业账号编号（查询母公司下订单：不传； 查询子公司下订单：传子公司账号）
        # :param pageLen	String	Y	50	每页条数，默认10，最大100

        FuncName = self.queryOrderItem.__doc__

        data = StandConfig.QueryOrderItem.data
        appMethod = StandConfig.QueryOrderItem.method

        data = data % ({"startDate":startDate,"endDate":endDate,"pageNum":pageNum,"pageLen":pageLen,"orderItemStatus":orderItemStatus,"companyCusNo":companyCusNo,"dateType":dateType})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getPeriodLimit(self,userAccount):
        """客户账期额度查询接口"""
        # sumPrice:        额度总额
        # leftPrice:       可用额度

        FuncName = self.getPeriodLimit.__doc__

        data = StandConfig.GetPeriodLimit.data
        appMethod = StandConfig.GetPeriodLimit.method
        data = data % ({"userAccount":userAccount})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getBill(self,types='',info='',pageNum='1',pgSize='10'):
        """获取账单信息接口"""
        # :param type: String	Y	1	入参类型：1-账单编码 2-订单号
        # :param info: String	Y	10000000	账单编码或订单号
        # :param pageNum: String	N	1	页码，默认第一页
        # :param pgSize: String	N	10	每页条数，默认10条

        FuncName = self.getBill.__doc__

        data = StandConfig.GetBill.data
        appMethod = StandConfig.GetBill.method

        data = data % ({"type":types,"info":info,"pageNum":pageNum,"pgSize":pgSize})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getOrderLogist(self,orderId,orderItemId,skuId=""):
        """获取订单物流详情"""

        FuncName = self.getOrderLogist.__doc__

        data = StandConfig.GetOrderLogist.data
        appMethod = StandConfig.GetOrderLogist.method

        data = data % ({"orderId":orderId,"orderItemId":orderItemId,"skuId":skuId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getOrderLogistNew(self,orderId,orderItemId,skuId=""):
        """获取订单物流详情（新）"""

        FuncName = self.getOrderLogistNew.__doc__

        data = StandConfig.GetOrderLogistNew.data
        appMethod = StandConfig.GetOrderLogistNew.method

        data = data % ({"orderId":orderId,"orderItemId":orderItemId,"skuId":skuId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getShipTime(self,skuId='',cityId="025",districtId="01",townId="99",addrDetail=""):
        """物流时效接口"""

        FuncName = self.getShipTime.__doc__

        data = StandConfig.GetShipTime.data
        appMethod = StandConfig.GetShipTime.method

        skuIds = ""
        for i in skuId.split(","):
            skuIds = skuIds + "<skuIds><skuId>{}</skuId></skuIds>".format(i)

        data = data % ({"skuIds":skuIds,"cityId":cityId,"districtId":districtId,"townId":townId,"addrDetail":addrDetail})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getShipCarriage(self,skuId,piece="1",cityId="025",districtId="11",townId="",addrDetail=""):
        """物流运费信息"""

        FuncName = self.getShipCarriage.__doc__

        data = StandConfig.GetShipCarriage.data
        appMethod = StandConfig.GetShipCarriage.method

        data = data % ({"skuId":skuId,"piece":piece,"cityId":cityId,"districtId":districtId,"townId":townId,"addrDetail":addrDetail})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def conFacProduct(self,orderId,skuId="",confirmTime=''):
        """厂送商品确认收货接口"""
        #说明：一单多品确认收货时，skuId="121347748,121347884"

        FuncName = self.conFacProduct.__doc__

        data = StandConfig.ConFacProduct.data
        appMethod = StandConfig.ConFacProduct.method

        if confirmTime=='':
            confirmTime=self.nowtime

        skuIdinfo = ""
        for i in skuId.split(","):
            skuIdinfo = skuIdinfo + "<skuConfirmList><confirmTime>{}</confirmTime><skuId>{}</skuId></skuConfirmList>".format(confirmTime,i)

        data = data % ({"orderId":orderId,"skuIdinfo":skuIdinfo})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getLogistDetail(self,orderId,orderItemId):
        """获取订单包裹信息接口"""

        FuncName = self.getLogistDetail.__doc__

        data = StandConfig.Getlogistdetail.data
        appMethod = StandConfig.Getlogistdetail.method

        data = data % ({"orderId":orderId,"orderItemId":orderItemId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def confirmInvoice(self,gcOrderNo='',invoiceType=2,invoiceContent=22,title='测试补开发票',taxNo='111111111111111', \
                       regTel='18767890345',companyName='中国苏宁',regAdd='江苏省南京市玄武区雨花路',regBank='宇宙银行', \
                       regAccount='6223456122453335111244553',consigneeName='张三',consigneeMobileNum='18767890345', \
                       address='北京市朝阳区望京东路18号',markId='',remark='11'):
        """政企订单补开发票"""
        # invoiceType            发票类型 2：普票 ，6：增票
        # invoiceContent         发票内容 1:明细，3：电脑配件，19:耗材，22：办公用品，25：电器，28：数码
        # taxNo                  纳税人识别号（传入增票信息时必传）
        # regAdd                 注册地址（传入增票信息时必传）
        # regBank                开户银行（传入增票信息时必传）
        # regAccount             银行账户（传入增票信息时必传）
        # consigneeName          发票收件人姓名
        # consigneeMobileNum     发票收件人手机号
        # :return:
        #         invoiceAmount	     开票金额
        #         invoiceStatus      开票状态 1 成功，0 失败
        #         invoiceType        发票类型 2 普票，6 增票
        #         orderNo            苏宁B2C系统订单号
        #         status             订单行状态 1:审核中 ，2:待发货 ，3:已发货 ，4:已完成 ，5:已取消 ，6:已退货 ， 7:订单异常 ， 8：审核不通过


        FuncName = self.confirmInvoice.__doc__

        data = StandConfig.ConfirmInvoice.data
        appMethod = StandConfig.ConfirmInvoice.method

        orderInfoDTO = ''
        for i in gcOrderNo.split(","):
            orderInfoDTO = orderInfoDTO + '<orderInfoDTO><gcOrderNo>{}</gcOrderNo></orderInfoDTO>'.format(i)

        data = data % ({"orderInfoDTO": orderInfoDTO, "invoiceType": invoiceType, "invoiceContent": invoiceContent,\
                        "title": title, "taxNo": taxNo, "regTel": regTel, "companyName": companyName, "regAdd": regAdd,\
                        "regBank": regBank, "regAccount": regAccount, "consigneeName": consigneeName,\
                        "consigneeMobileNum": consigneeMobileNum, "address": address,"markId":markId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def eleInvoice(self,orderId,orderItemId='',skuId=''):
        """电子发票查询接口"""

        FuncName = self.eleInvoice.__doc__

        data = StandConfig.EleInvoice.data
        appMethod = StandConfig.EleInvoice.method

        data = data % ({"orderItemId": orderItemId, "skuId": skuId, "orderId": orderId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getInvoice(self,field='',type=''):
        """发票信息查询接口"""
        # type    1.政企订单号    2.政企订单行号

        FuncName = self.getInvoice.__doc__

        data = StandConfig.GetInvoice.data
        appMethod = StandConfig.GetInvoice.method

        data = data % ({"field": field, "type": type})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def invoiceLogistic(self,parameter='',parameterInvoice='',type='1',pageNum=''):
        """
        发票物流接口
        :param parameter: Y markId
        :param parameterInvoice:  N 发票id
        :param Type:  Y 查询类型 1-申请单号 2-订单号 3-发票 20191014版本仅支持申请单号查物流
        :param pageNum: N 页数：默认传1
        :return:
        """
        FuncName = self.invoiceLogistic.__doc__
        data = StandConfig.InvoiceLogistic.data
        appMethod = StandConfig.InvoiceLogistic.method

        data = data % ({"parameter": parameter,"parameterInvoice":parameterInvoice,"type": type,"pageNum":pageNum})
        # print(data)
        sign = self.GetSign(self.appKey, self.appSecret, appMethod=appMethod, reqTime=self.nowtime, data=data)
        self.reqData.update({"appKey": self.appKey, "appMethod": appMethod, "reqParam": data,
                             "appRequestTime": self.nowtime, "signInfo": sign})
        resp = self.common.post(url=self.host, data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def signInvoice(self,parameter='',confirmType=''):
        """
        发票签收接口
        :param parameter:  Y 申请单号或订单号
        :param confirmType:  Y 确认类型 1-申请单号 2-订单号
        :return: 成功or失败
        """
        FuncName = self.signInvoice.__doc__
        data = StandConfig.SignInvoice.data
        appMethod = StandConfig.SignInvoice.method

        data = data % ({"parameter": parameter,  "confirmType": confirmType})
        print(data)
        sign = self.GetSign(self.appKey, self.appSecret, appMethod=appMethod, reqTime=self.nowtime, data=data)
        self.reqData.update({"appKey": self.appKey, "appMethod": appMethod, "reqParam": data,
                             "appRequestTime": self.nowtime, "signInfo": sign})
        resp = self.common.post(url=self.host, data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata


    def getFullAddress(self):
        """全量地址接口"""

        FuncName = self.getFullAddress.__doc__

        data = StandConfig.GetfullAddress.data
        appMethod = StandConfig.GetfullAddress.method

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getPaymentWay(self,provinceCode='100',cityCode='025',districtCode='03',townCode='99',skuId='',payAmount='88.00'):
        """是否支持货到付款接口"""
        # :param payAmount: String	Y	88.00	支付总金额，多个商品一起提交订单，传和
        # :return codCash	String	Y	是否支持货到付款现金；Y-支持；N-不支持
        #         codPos	String	Y	是否支持货到付款POS；Y-支持，N-不支持

        FuncName = self.getPaymentWay.__doc__

        data = StandConfig.GetPaymentWay.data
        appMethod = StandConfig.GetPaymentWay.method

        data = data % ({"provinceCode":provinceCode,"cityCode":cityCode,"districtCode":districtCode,\
                        "townCode":townCode,"skuId":skuId,"payAmount":payAmount})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getPriceMessage(self):
        """价格变动消息查询接口"""

        FuncName = self.getPriceMessage.__doc__

        data = StandConfig.GetPriceMessage.data
        appMethod = StandConfig.GetPriceMessage.method


        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def createOnlinePay(self,orderId,channelType='1',backUrl='http://www.suning.com',payway=''):
        """在线支付接口"""

        # orderId         政企订单号
        # channelType     渠道，1代表PC，2代表Wap
        # backUrl         支付成功的回跳链接（订单详情）
        # return：
        #        payUrl   支付链接

        FuncName = self.createOnlinePay.__doc__

        data = StandConfig.CreateOnlinePay.data
        appMethod = StandConfig.CreateOnlinePay.method

        data = data % ({"orderId": orderId, "channelType": channelType, "backUrl": backUrl})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        try:

            tmp = json.loads(redata)

            payUrl = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["payUrl"]
            merchantNo = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["merchantNo"]
            merchantDomain = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["merchantDomain"]
            publicKeyIndex = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["publicKeyIndex"]
            signature = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["signature"]
            notifyUrl = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["notifyUrl"]
            returnUrl = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["returnUrl"]
            submitTime = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["submitTime"]

            buyerUserNo = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["buyerUserNo"]
            buyerAlias = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["buyerAlias"]
            buyerMerchantLoginName = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["buyerMerchantLoginName"]
            buyerMerchantUserNo = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["buyerMerchantUserNo"]
            payOtherFlag = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["payOtherFlag"]
            orders = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["orders"]
            orders = json.dumps(orders, separators=(',', ':'))

            body = []
            header = '''
            <!DOCTYPE html>
            <html>
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
            <body>
            '''
            body.append(header)

            reUrl = '<form action="%(payUrl)s" method="post">' % ({'payUrl': payUrl})
            body.append(reUrl)
            merchantNo = 'merchantNo:<input type="text" name="merchantNo" value="%(merchantNo)s"><br>' % (
            {'merchantNo': merchantNo})
            body.append(merchantNo)
            merchantDomain = 'merchantDomain:<input type="text" name="merchantDomain" value="%(merchantDomain)s"><br>' % (
                {'merchantDomain': merchantDomain})
            body.append(merchantDomain)
            publicKeyIndex = 'publicKeyIndex:<input type="text" name="publicKeyIndex" value="%(publicKeyIndex)s"><br>' % (
                {'publicKeyIndex': publicKeyIndex})
            body.append(publicKeyIndex)
            signature = 'signature:<input type="text" name="signature" value="%(signature)s"><br>' % (
            {'signature': signature})
            body.append(signature)
            signAlgorithm = 'signAlgorithm:<input type="text" name="signAlgorithm" value="RSA"><br>'
            body.append(signAlgorithm)
            inputCharset = 'inputCharset:<input type="text" name="inputCharset" value="UTF-8"><br>'
            body.append(inputCharset)
            notifyUrl = 'notifyUrl:<input type="text" name="notifyUrl" value="%(notifyUrl)s"><br>' % (
            {'notifyUrl': notifyUrl})
            body.append(notifyUrl)
            returnUrl = 'returnUrl:<input type="text" name="returnUrl" value="%(returnUrl)s"><br>' % (
            {'returnUrl': returnUrl})
            body.append(returnUrl)
            submitTime = 'submitTime:<input type="text" name="submitTime" value="%(submitTime)s"><br>' % (
            {'submitTime': submitTime})
            body.append(submitTime)
            buyerUserNo = 'buyerUserNo:<input type="text" name="buyerUserNo" value="%(buyerUserNo)s"><br>' % (
            {'buyerUserNo': buyerUserNo})
            body.append(buyerUserNo)
            buyerAlias = 'buyerAlias:<input type="text" name="buyerAlias" value="%(buyerAlias)s"><br>' % (
            {'buyerAlias': buyerAlias})
            body.append(buyerAlias)
            buyerMerchantLoginName = 'buyerMerchantLoginName:<input type="text" name="buyerMerchantLoginName" value="%(buyerMerchantLoginName)s"><br>' % (
                {'buyerMerchantLoginName': buyerMerchantLoginName})
            body.append(buyerMerchantLoginName)
            buyerMerchantUserNo = 'buyerMerchantUserNo:<input type="text" name="buyerMerchantUserNo" value="%(buyerMerchantUserNo)s"><br>' % (
                {'buyerMerchantUserNo': buyerMerchantUserNo})
            body.append(buyerMerchantUserNo)
            payOtherFlag = 'payOtherFlag:<input type="text" name="payOtherFlag" value="%(payOtherFlag)s"><br>' % (
            {'payOtherFlag': payOtherFlag})
            body.append(payOtherFlag)

            if payway == '020':
                version1 = tmp["sn_responseContent"]["sn_body"]["createOnlinepay"]["version"]
                version = 'version:<input type="text" name="version" value="%(version)s"><br>' % ({'version': version1})
                body.append(version)
            orders = '''orders:<input type="text" name="orders" value='%(orders)s'><br>''' % ({'orders': orders})
            body.append(orders)

            ender = """<input type="submit" value="Submit">
            </form> 
            </body>
            </html>"""
            body.append(ender)
            with open(self.common.get_desktop()+"\payonline.html", "w") as file:
                file.truncate()
            with open(self.common.get_desktop()+"\payonline.html", "a") as file:
                for i in body:
                    file.write(i + '\n')
        except Exception:
            raise tmp


        print(redata)

        return redata

    def preDepositBalance(self):
        """查询预存款金额接口"""

        FuncName = self.preDepositBalance.__doc__

        data = StandConfig.PreDepositBalance.data
        appMethod = StandConfig.PreDepositBalance.method


        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getMessage(self,type):
        """查询消息接口"""

        # type 消息类型
        # 10 - 商品池          上架1、下架2、添加0、删除4、修改3
        # 11 - 订单            实时创建1、预占成功2、确认预占3、取消预占4、异常订单取消5　
        # 12 - 物流            商品出库1、商品妥投2、商品拒收3、商品退货4
        # 13 - 目录            添加0、修改1、删除2
        # 14 - 服务状态消息     待服务1、服务完成2、服务取消3
        # 16 - 支付状态         已支付1、订单已取消2、订单已失效3
        # 17 - 账单消息         新增1

        FuncName = self.getMessage.__doc__

        data = StandConfig.GetMessage.data
        appMethod = StandConfig.GetMessage.method

        data = data % ({"type": type})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def deleteMessage(self,id):
        """删除消息接口"""


        FuncName = self.deleteMessage.__doc__

        data = StandConfig.DeleteMessage.data
        appMethod = StandConfig.DeleteMessage.method

        data = data % ({"id": id})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def getServiceRates(self, orderId,orderItemId=''):
        """查询服务进度信息"""

        # return：
        #         serviceStatus   服务进度
        #         1初始状态、2处理中状态、3服务完成、4取消状态、5退货中状态、
        #         6退货完成、7支付完成、70支付中、8支付失败

        FuncName = self.getServiceRates.__doc__

        data = StandConfig.GetServicerates.data
        appMethod = StandConfig.GetServicerates.method

        itemid_tmp = ""

        for itemid in orderItemId.split(","):
            itemid_tmp = itemid_tmp + ("<orderItemIds><orderItemId>%s</orderItemId></orderItemIds>" % itemid)

        data = data % ({"orderId": orderId,"orderItemIds":itemid_tmp})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata


    def setSecretKey(self, publicKey='', type=''):
        """设置公钥信息接口"""

        # publicKey   公钥
        # type        操作类型 0:添加 1:更新

        FuncName = self.setSecretKey.__doc__

        data = StandConfig.SetSecretKey.data
        appMethod = StandConfig.SetSecretKey.method

        data = data % ({"publicKey": publicKey, "type": type})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata


    def getCardSecretKey(self, orderId='', pageNumber='50', currentPage='1'):
        """在线获取礼品卡卡密接口"""

        # gcOrderNo      政企订单号
        # pageNumber     每页记录数(不能大于100)
        # currentPage	 当前页数


        FuncName = self.getCardSecretKey.__doc__

        data = StandConfig.GetCardSecretkey.data
        appMethod = StandConfig.GetCardSecretkey.method

        data = data % ({"gcOrderNo": orderId, "pageNumber": pageNumber, "currentPage": currentPage})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def logNumSubmit(self,orderId='',gc_item_no='',skuId='',sheetId='',serviceType='1',expressCompanyName='顺丰速运',expressOrderId='201905171705',online='N'):
        """厂送寄退物流提报接口"""
        #说明：gc_item_no=''时，则提报订单所有行，gc_item_no不为空时，则提报指定行
        #     online='Y'时，skuId，sheetId需要手动填写

        # sheetId		            售后服务单号
        # expressCompanyName		顺丰快递公司名称
        # expressOrderId			快递单号
        # serviceType               服务类型   1-退货,2-换货

        FuncName = self.logNumSubmit.__doc__

        data = StandConfig.LogNumSubmit.data
        appMethod = StandConfig.LogNumSubmit.method

        if online =='N':
            if gc_item_no=='':
                orderItemIds=""

                result=self.mysql.searchs("select gc_item_no,commdty_code from srcorder_item where gc_order_no='%s'"%orderId)

                for k in result:
                    gc_item_no = str(k[0])
                    commdty_code = str(k[1])


                    sheetId = self.mysql.searchs("select gong_dan from gcapi_after_sales where gc_item_no='{}' order by id desc".format(gc_item_no))

                    orderItemIds= orderItemIds+"<orderItemIds><orderItemId>%(orderItem)s</orderItemId><skuId>%(skuId)s</skuId>\
                    <sheetId>%(sheetId)s</sheetId><expressCompanyName>%(expressCompanyName)s</expressCompanyName>\
                    <expressOrderId>%(expressOrderId)s</expressOrderId></orderItemIds>"%(\
                    {"orderItem":gc_item_no,"skuId":commdty_code,"sheetId":list(sheetId)[0][0],"expressCompanyName":expressCompanyName,\
                     "expressOrderId":expressOrderId})
            else:
                orderItemIds = ""
                for c in gc_item_no.split(","):
                    result = self.mysql.searchs("select commdty_code from srcorder_item where gc_item_no='%s'" % c)
                    gc_item_no = c
                    commdty_code = str(result[0][0])

                    sheetId = self.mysql.searchs(
                        "select gong_dan from gcapi_after_sales where gc_item_no='{}' order by id desc".format(gc_item_no))

                    orderItemIds = orderItemIds + "<orderItemIds><orderItemId>%(orderItem)s</orderItemId><skuId>%(skuId)s</skuId>\
                                    <sheetId>%(sheetId)s</sheetId><expressCompanyName>%(expressCompanyName)s</expressCompanyName>\
                                    <expressOrderId>%(expressOrderId)s</expressOrderId></orderItemIds>" % ( \
                        {"orderItem": gc_item_no, "skuId": commdty_code, "sheetId": list(sheetId)[0][0],
                         "expressCompanyName": expressCompanyName, \
                         "expressOrderId": expressOrderId})
        else:
            orderItemIds = "<orderItemIds><orderItemId>%(orderItem)s</orderItemId><skuId>%(skuId)s</skuId>\
                                <sheetId>%(sheetId)s</sheetId><expressCompanyName>%(expressCompanyName)s</expressCompanyName>\
                                <expressOrderId>%(expressOrderId)s</expressOrderId></orderItemIds>" % ( \
                        {"orderItem": gc_item_no, "skuId": skuId, "sheetId": sheetId,
                         "expressCompanyName": expressCompanyName, \
                         "expressOrderId": expressOrderId})

        data = data % ({"orderId":orderId,"orderItemIds":orderItemIds,"serviceType":serviceType})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata


    def queryServicescheDule(self, orderId='',orderItem='',skuId='',sheetId='',serviceType='1',online='N'):
        """售后进度查询接口"""

        # afterSrvStatus	 当前售后状态 0 退货待处理 4 顾客已申请寄货 7 同意退货     8 不同意退货 9 顾客寄货
        #                               10 同意退款  11 拒绝退款     15 实际退款成功 17 取消退货
        # afterSrvSch	     售后进度描述
        # serviceType        服务类型     1 - 退货，2 - 换货，3 - 维修
        #     online='Y'时，orderItem,skuId,sheetId需要手动填写

        FuncName = self.queryServicescheDule.__doc__

        data = StandConfig.QueryServicescheDule.data
        appMethod = StandConfig.QueryServicescheDule.method

        if online=='N':
            orderItemIdsinfo = ""

            result = self.mysql.searchs(
                "select gc_item_no,commdty_code,factory_send from srcorder_item where gc_order_no='%s'" % orderId)

            for k in result:
                gc_item_no = str(k[0])
                commdty_code = str(k[1])
                factory_send = str(k[2])

                if serviceType=='3':
                    sheetId = self.mysql.searchs(
                        "select gong_dan from gcapi_after_sales where gc_item_no='{}' order by id desc".format(gc_item_no))

                    orderItemIdsinfo = orderItemIdsinfo + "<orderItemIds><sheetId>{}</sheetId><orderItemId>{}</orderItemId>\
                                        <skuId>{}</skuId></orderItemIds>".format(list(sheetId)[0][0], gc_item_no,
                                                                                 commdty_code)
                else:
                    if factory_send=='2':
                        orderItemIdsinfo = orderItemIdsinfo + "<orderItemIds><sheetId></sheetId><orderItemId>{}</orderItemId>\
                                                        <skuId>{}</skuId></orderItemIds>".format(gc_item_no, commdty_code)
                    else:
                        sheetId = self.mysql.searchs(
                            "select gong_dan from gcapi_after_sales where gc_item_no='{}' order by id desc".format(gc_item_no))
                        if list(sheetId):
                            orderItemIdsinfo = orderItemIdsinfo + "<orderItemIds><sheetId>{}</sheetId><orderItemId>{}</orderItemId>\
                                                <skuId>{}</skuId></orderItemIds>".format(list(sheetId)[0][0],gc_item_no,commdty_code)
                        else:
                            orderItemIdsinfo = orderItemIdsinfo + "<orderItemIds><sheetId></sheetId><orderItemId>{}</orderItemId>\
                                                                            <skuId>{}</skuId></orderItemIds>".format( gc_item_no, commdty_code)
        else:
            orderItemIdsinfo = "<orderItemIds><sheetId>{}</sheetId><orderItemId>{}</orderItemId>\
                                <skuId>{}</skuId></orderItemIds>".format(sheetId,orderItem,skuId)

        data = data % ({"orderId": orderId, "orderItemIdsinfo": orderItemIdsinfo,"serviceType":serviceType})
        # print(data)
        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def repairMethodQuery(self,orderId='',orderItemId='',skuId='',cityId='025',countyId='01'):
        """维修方式查询接口"""
        # repairType   维修类型编码（00：不支持维修；01:揽件寄修；02: 送修；04:上门维修；09：厂家维修）

        FuncName = self.repairMethodQuery.__doc__

        data = StandConfig.RepairMethodQuery.data
        appMethod = StandConfig.RepairMethodQuery.method
        data = data % ({"orderId":orderId,"orderItemId":orderItemId,"skuId":skuId,"cityId":cityId,"countyId":countyId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def afterServiceQuery(self,orderId='',orderItemId='',skuId='',cityId='025',countyId='01'):
        """售后服务类型查询接口"""
        # srvType    服务类型（1-退货，2-换货，3-维修，4-无售后服务）

        FuncName = self.afterServiceQuery.__doc__

        data = StandConfig.AfterServiceQuery.data
        appMethod = StandConfig.AfterServiceQuery.method

        skuId = list(skuId.split(","))
        skus = ''
        k = 0

        for i in orderItemId.split(","):
            skus = skus + "<skus><orderItemId>{}</orderItemId><skuId>{}</skuId></skus>".format(i,skuId[k])
            k = k+1

        data = data % ({"orderId":orderId,"cityId":cityId,"countyId":countyId,"skus":skus})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def applyRepairGoods(self,orderId='',orderItemId='',skuId='',num='1',serviceTime='20190615090000', \
                          receiverName='张三',phoneNum='010-88888888',mobPhoneNum='15811084770',\
                          srvMemo='带一根1米长水管',orderMemo='洗衣机滚筒电机损坏', \
                          provinceId='100',cityId='025',countyId='01',townId='99',address='望京东路8号'):
        """维修申请接口"""
        # srvMemo   服务订单备注

        FuncName = self.applyRepairGoods.__doc__

        data = StandConfig.ApplyRepairGoods.data
        appMethod = StandConfig.ApplyRepairGoods.method
        data = data % ({"orderId":orderId,"orderItemId":orderItemId,"skuId":skuId,"num":num,\
                        "serviceTime":serviceTime,"receiverName":receiverName,"phoneNum":phoneNum,\
                        "mobPhoneNum":mobPhoneNum,"srvMemo":srvMemo,"orderMemo":orderMemo,\
                        "provinceId":provinceId,"cityId":cityId,"countyId":countyId,"townId":townId,\
                        "address":address})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def cancelRepairGoods(self,orderId='',orderItemId='',skuId='',sheetId='',cancelReason='不需要维修了'):
        """取消维修申请接口"""

        FuncName = self.cancelRepairGoods.__doc__

        data = StandConfig.CancelRepairGoods.data
        appMethod = StandConfig.CancelRepairGoods.method
        data = data % ({"orderId":orderId,"orderItemId":orderItemId,"skuId":skuId,"sheetId":sheetId,\
                        "cancelReason":cancelReason})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def applyexChangeGoods(self,orderId='',orderItemId='',skuId='',num='1',reasonDetails='屏幕损坏'):
        """换货申请接口"""

        # 说明：支持换多个品，如skuId='121347748,121347746',num='1,2'
        # 则121347748换1个，121347746换2个

        # reasonDetails    退货详细原因厂送商品退货时需要，非必填

        FuncName = self.applyexChangeGoods.__doc__

        data = StandConfig.ApplyexChangeGoods.data
        appMethod = StandConfig.ApplyexChangeGoods.method

        orderItemIds=''
        skuId = skuId.split(",")
        num = num.split(",")
        k=0

        for orderItem in orderItemId.split(","):
            orderItemIds = orderItemIds + "<orderItems><orderItemId>{}</orderItemId><skuId>{}</skuId><num>{}</num>\
            <reasonDetails>{}</reasonDetails></orderItems>".format(orderItem,skuId[k],num[k],reasonDetails)
            k = k + 1

        data = data % ({"orderId":orderId,"orderItemIds":orderItemIds})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def cancelRetchgGoods(self,orderId='',orderItemId='',skuId='',operateType='1'):
        """取消退换货接口"""
        #支持批量处理orderItemId、skuId需要一一对应，使用","隔开
        #operateType    1-取消退货；2-取消换货

        FuncName = self.cancelRetchgGoods.__doc__

        data = StandConfig.CancelRetchgGoods.data
        appMethod = StandConfig.CancelRetchgGoods.method

        orderItems=''
        orderItemId = orderItemId.split(",")
        k = 0
        for i in skuId.split(","):
            orderItems=orderItems+'<orderItemId>{}</orderItemId><skuId>{}</skuId>'.format(orderItemId[k],i)
            k = k + 1

        data = data % ({"orderId":orderId,"orderItems":orderItems,"operateType":operateType})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def aliPay(self,orderIds='',channelType='PC',backUrl='http://www.suning.com',mobileOS='01',mobileModel='苹果6'):
        """支付宝支付接口"""

        # orderId         政企订单号
        # channelType     渠道，PC/WAP/SDK
        # backUrl         支付成功的回跳链接（订单详情）
        # mobileOS        01代表IOS；02代表安卓；
        # mobileModel     手机型号
        # return：
        #        payUrl   支付链接

        FuncName = self.aliPay.__doc__

        data = StandConfig.AliPay.data
        appMethod = StandConfig.AliPay.method
        gc_order_no  = ''
        for orderId in orderIds.split(","):
            orderIdCup =  "<orderIds><orderId>" + orderId + "</orderId></orderIds>"
            gc_order_no = gc_order_no + orderIdCup

        data = data % ({"mobileOS":mobileOS,"mobileModel":mobileModel,"channelType": channelType, "backUrl": backUrl,"orderId":gc_order_no})
        print(data)
        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]

        try:

            tmp = json.loads(redata)

            service = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["service"]
            partner = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["partner"]
            inputCharset = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["inputCharset"]
            signType = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["signType"]
            sign = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["sign"]
            notifyUrl = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["notifyUrl"]

            outTradeNo = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["outTradeNo"]

            subject = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["subject"]
            totalFee = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["totalFee"]
            sellerId = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["sellerId"]
            paymentType = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["paymentType"]
            itBPay = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["itBPay"]
            rnCheck = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["rnCheck"]
            disablePaymethod = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["disablePaymethod"]

            body = []
            if channelType!='SDK':
                returnUrl = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["returnUrl"]

                header = '''
                <!DOCTYPE html>
                <html>
                <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
                <body>
                '''

                body.append(header)
                payUrl="https://mapi.alipay.com/gateway.do?_input_charset=utf-8"
                reUrl = '<form name="alipaysubmit" id="alipaysubmit" method="post" action="{}">'.format(payUrl)
                body.append(reUrl)
                service = 'service:<input type="text" name="service" value="{}"><br>'.format(service)
                body.append(service)
                partner = 'partner:<input type="text" name="partner" value="{}"><br>'.format(partner)
                body.append(partner)
                inputCharset = 'inputCharset:<input type="text" name="_input_charset" value="{}"><br>'.format(inputCharset)
                body.append(inputCharset)
                signType = 'signType:<input type="text" name="sign_type" value="{}"><br>'.format(signType)
                body.append(signType)
                sign = 'sign:<input type="text" name="sign" value="{}"><br>'.format(sign)
                body.append(sign)
                notifyUrl = 'notifyUrl:<input type="text" name="notify_url" value="{}"><br>'.format(notifyUrl)
                body.append(notifyUrl)
                returnUrl = 'returnUrl:<input type="text" name="return_url" value="{}"><br>'.format(returnUrl)
                body.append(returnUrl)
                outTradeNo = 'outTradeNo:<input type="text" name="out_trade_no" value="{}"><br>'.format(outTradeNo)
                body.append(outTradeNo)
                subject = 'subject:<input type="text" name="subject" value="{}"><br>'.format(subject)
                body.append(subject)
                totalFee = 'totalFee:<input type="text" name="total_fee" value="{}"><br>'.format(totalFee)
                body.append(totalFee)
                sellerId = 'sellerId:<input type="text" name="seller_id" value="{}"><br>'.format(sellerId)
                body.append(sellerId)
                paymentType = 'paymentType:<input type="text" name="payment_type" value="{}"><br>'.format(paymentType)
                body.append(paymentType)
                itBPay = 'itBPay:<input type="text" name="it_b_pay" value="{}"><br>'.format(itBPay)
                body.append(itBPay)
                rnCheck = 'rnCheck:<input type="text" name="rn_check" value="{}"><br>'.format(rnCheck)
                body.append(rnCheck)
                disablePaymethod = 'disablePaymethod:<input type="text" name="disable_paymethod" value="{}"><br>'.format(disablePaymethod)
                body.append(disablePaymethod)

                if channelType == 'WAP':
                    appPay = tmp["sn_responseContent"]["sn_body"]["createAlipay"]["appPay"]
                    appPay = 'appPay:<input type="text" name="app_pay" value="{}"><br>'.format(appPay)
                    body.append(appPay)

                ender = """<input type="submit" value="提交">
                </form> 
                </body>
                </html>"""
                body.append(ender)

                with open(self.common.get_desktop()+"\Alipayonline.html", "w",encoding='utf-8') as file:
                    file.truncate()
                with open(self.common.get_desktop()+"\Alipayonline.html", "a",encoding='utf-8') as file:
                    for i in body:
                        file.write(i + '\n')
            else:
                body = '_input_charset="{}"&disable_paymethod="{}"&it_b_pay="{}"&notify_url="{}"&out_trade_no="{}"&partner="{}"&' \
                       'payment_type="{}"&rn_check="{}"&seller_id="{}"&service="{}"&sign="{}"&sign_type="{}"&subject="{}"&total_fee="{}"'.format(\
                    "utf-8",disablePaymethod,itBPay,notifyUrl,outTradeNo,partner,paymentType,rnCheck,sellerId,service,urlencode(sign),\
                    signType,subject,totalFee)
                print("SDK调起链接参数：" + body)

        except Exception:
            raise tmp


        print("支付宝接口返回参数：" + redata)

        return redata


    def serialnoQuery(self,orderId='',orderItemId='',skuId=''):
        """订单SN码查询接口"""

        FuncName = self.serialnoQuery.__doc__

        data = StandConfig.SerialnoQuery.data
        appMethod = StandConfig.SerialnoQuery.method

        data = data % ({"orderId":orderId,"orderItemId":orderItemId,"skuId":skuId})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def bankTransfer(self,phoneNum='',orderId=''):
        """查询订单sn码"""

        FuncName = self.bankTransfer.__doc__

        data = StandConfig.BankTransfer.data
        appMethod = StandConfig.BankTransfer.method

        orderIds = ""

        for i in orderId.split(","):
            orderIds = orderIds + "<orderIds><orderId>{}</orderId></orderIds>".format(i)

        data = data % ({"phoneNum":phoneNum,"orderIds":orderIds})

        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def poOrderId(self,orderId='',porderId='',orderItemId='',skuId='',num='',porderItemId='',remark=''):
        """po单信息提交"""


        FuncName = self.poOrderId.__doc__

        data = StandConfig.PoOrderId.data
        appMethod = StandConfig.PoOrderId.method

        skus=''

        skus = skus + "<skus><orderItemId>{}</orderItemId><skuId>{}</skuId><num>{}</num>\
        <porderItemId>{}</porderItemId><remark>{}</remark></skus>".format(orderItemId,skuId,num,porderItemId,remark)

        data = data % ({"orderId":orderId,"porderId":porderId,"skus":skus})

        # print(data)
        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def deleteinvoicebatch(self,markIds):
        '''发票批次撤回接口'''
        FuncName = self.deleteinvoicebatch.__doc__
        data = StandConfig.Deleteinvoicebatch.data
        appMethod = StandConfig.Deleteinvoicebatch.method
        batchNo = ""
        for markId in markIds.split(","):
            batchNo = batchNo + "<batchInfos><batchNo>{}</batchNo></batchInfos>".format(markId)

        data = data.format(batchNo)
        sign = self.GetSign(appKey = self.appKey, appSecret = self.appSecret, appMethod = appMethod, \
                            reqTime = self.nowtime, version = "v1.2", data = data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

    def getMarkIdInvoice(self,markId='',pageNumber='100',currentPage='1'):
        """发票批次查询接口"""
        FuncName = self.getMarkIdInvoice.__doc__
        data = StandConfig.GetMarkIdInvoice.data
        appMethod = StandConfig.GetMarkIdInvoice.method
        data = data % ({"markId": markId, "pageNumber": pageNumber,"currentPage": currentPage})
        # print(data)
        sign = self.GetSign(appKey=self.appKey, appSecret=self.appSecret, appMethod=appMethod, \
                            reqTime=self.nowtime, version="v1.2", data=data)
        self.reqData.update({"appKey": self.appKey, "appMethod": appMethod, "reqParam": data,
                             "appRequestTime": self.nowtime, "signInfo": sign})
        resp = self.common.post(url=self.host, data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        # print(resp)
        redata = resp["apiTestResp"]
        print(redata)

    def getsubcodeproducts(self,generalSku):
        '''获取通子码商品信息接口'''

        FuncName = self.getsubcodeproducts.__doc__
        data = StandConfig.Getsubcodeproducts.data
        appMethod  = StandConfig.Getsubcodeproducts.method

        data = data.format(generalSku)
        sign = self.GetSign(appKey = self.appKey, appSecret = self.appSecret, appMethod = appMethod, \
                            reqTime = self.nowtime, version = "v1.2", data = data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

    def invoiceSupplement(self,gcOrderNo='',gcItemNo='',markId='',remark='发票备注',invoiceType='6',invoiceContent='1',
                          title='测试环境发票抬头',taxNo='111222333444555',regTel='025-66996699',companyName='江苏苏宁软件',
                          regAdd='苏宁大道1号',regBank='苏宁银行',regAccount='123456789',consigneeName='收票人姓名',
                          consigneeMobileNum='13266666666',address='苏宁总部易购楼'):
        """
        补开发票接口（新）
        :param gcOrderNo: Y 政企订单号，支持批量，以“,”分割
        :param gcItemNo: Y 政企订单行号，支持批量，以“,”分割
        :param markId: Y 申请批次号
        :param remark: Y 发票备注
        :param invoiceType:  Y 发票类型 2-普票 4-电子发票 6-增票
        :param invoiceContent:  N 发票明细 1-明细
        :param title: Y 发票抬头
        :param taxNo: N 纳税人识别号（invoiceType为6时必填）
        :param regTel: N 注册电话（invoiceType为6时必填）
        :param companyName: N 公司名称（invoiceType为6时必填）
        :param regAdd: N 注册地址（invoiceType为6时必填）
        :param regBank: N 注册银行（invoiceType为6时必填）
        :param regAccount: N 银行账户（invoiceType为6时必填）
        :param consigneeName: N 收票人姓名（除电子发票外必填）
        :param consigneeMobileNum: Y 收票人手机号（电子发票必为手机号）
        :param address: N 收票人地址（除电子发票外必填）
        :return:
        """
        FuncName = self.invoiceSupplement.__doc__
        data = StandConfig.InvoiceSupplement.data
        appMethod = StandConfig.InvoiceSupplement.method
        orderInfoDTO = ''
        a = 0
        orderList = gcOrderNo.split(',')
        if markId == '':
            markId = self.timestmp
        if gcOrderNo == '' and gcItemNo == '':
            orderInfoDTO = orderInfoDTO + '<orderInfoDTO><gcOrderNo></gcOrderNo><gcItemNo></gcItemNo></orderInfoDTO>'

        elif gcOrderNo != '' and gcItemNo == '':
            for i in gcOrderNo.split(","):
                orderInfoDTO = orderInfoDTO + '<orderInfoDTO><gcOrderNo>{}</gcOrderNo></orderInfoDTO>'.format(i)
        elif  gcItemNo != '' and gcOrderNo == '':
            for j in gcItemNo.split(","):
                    orderInfoDTO = orderInfoDTO + '<orderInfoDTO><gcItemNo>{}</gcItemNo></orderInfoDTO>'.format(j)
        else :

            # for i in gcOrderNo.split(","):
            for j in gcItemNo.split(","):
                orderInfoDTO = orderInfoDTO + '<orderInfoDTO><gcOrderNo>{}</gcOrderNo></orderInfoDTO><orderInfoDTO><gcItemNo>{}</gcItemNo></orderInfoDTO>'.format(
                orderList[a], j)
                a = a + 1

        data = data % ({"orderInfoDTO": orderInfoDTO, "invoiceType": invoiceType, "invoiceContent": invoiceContent,\
                        "title": title, "taxNo": taxNo, "regTel": regTel, "companyName": companyName, "regAdd": regAdd,\
                        "regBank": regBank, "regAccount": regAccount, "consigneeName": consigneeName,\
                        "consigneeMobileNum": consigneeMobileNum, "address": address,"markId":markId,"remark":remark})

        print(data)
        sign = self.GetSign(appKey=self.appKey, appSecret=self.appSecret, appMethod=appMethod, \
                            reqTime=self.nowtime, version="v1.2", data=data)
        self.reqData.update({"appKey": self.appKey, "appMethod": appMethod, "reqParam": data,
                             "appRequestTime": self.nowtime, "signInfo": sign})
        resp = self.common.post(url=self.host, data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)


    def mixOrder_NHXD(self,skuIds,isservFee,companyCustNo="",nums='1',orderType=0,hopeArrivalTime='',\
                        isInvoice=1,payType="20",invoiceType=4,\
                    province="100",city="025",county="01",townId='99',address='南京玄武1'):
        """农行小豆创建订单接口"""
        #说明：下多个品时，skuIds="121347748,121347746",nums="1,2"
        #则121347748购买1个，121347746购买2个

        # companyCustNo: 子账号会员编码
        # orderType: 订单类型(0.实时型订单1.预占型订单)
        # isInvoice: 是否开发票(1 = 开，0 = 不开)
        # payType: 支付方式(20-混合支付)
        # invoiceType: 发票类型：1-增值税专票;2-普票（即卷票，票随货走）;
        #                       3-增值税普票（即平推式普票，票货分离）；4-电子发票

        FuncName = self.mixOrder_NHXD.__doc__

        tradeNo = "mixNHXD" + str(self.timestmp) + str(random.randint(1,1000))
        data = StandConfig.Mixpayorder_NHXD.data
        appMethod = StandConfig.Mixpayorder_NHXD.method
        skuInfo = ""
        amount = 0
        servFee = 0
        i=0
        sku = skuIds.split(",")

        for num in nums.split(','):
            priceInfo = self.getPrice(sku[i],city)
            price = list(priceInfo.values())[0]
            skuInfo = skuInfo + "<sku><num>%(num)s</num><skuId>%(sku)s</skuId>\
                <unitPrice>%(price)s</unitPrice></sku>" % ({"num": num, "sku": sku[i], "price": price})
            val = float(price) * int(num)
            amount = float('%.2f' % Decimal(amount)) + float('%.2f' % Decimal(val))
            amount = float('%.2f' %amount)
            i = i + 1

        if isservFee == 'Y':
            if amount < 86:
                servFee = 5

        pay2931 = 0.01
        pay9005 = float(Decimal(str(amount)) - Decimal(str(pay2931)))


        data = data % (
        {"province": province, "city": city, "county": county, "townId":townId,"address":address + tradeNo,"payTpye": payType, "orderType": orderType,
         "isInvoice": isInvoice, "invoiceType": invoiceType, "tradeNo": tradeNo, "companyCustNo": companyCustNo,"hopeArrivalTime":hopeArrivalTime,
         "servFee": servFee, "amount": float('%.2f' % Decimal(amount)), "skuInfo": skuInfo,"9005":pay9005,"2931":pay2931})
        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)

        return redata

    def addabcpay(self,orderIds,channelType='3'):
        """'快E付'支付"""
        #说明 ： 快E付支付
        #入参证企订单号
        # channelType   终端类型  3-SDK
        FuncName = self.addabcpay.__doc__
        data = StandConfig.Addabcpay.data
        appMethod = StandConfig.Addabcpay.method
        orderIdLists = ''
        for orderId in orderIds.split(","):
            orderIdList = "<orderIds><orderId>{}</orderId></orderIds>".format(orderId)
            orderIdLists = orderIdLists + orderIdList
        data = data % ({"channelType":channelType,"orderIdList":orderIdLists})
        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        print(data)
        redata = resp["apiTestResp"]
        print(redata)
        return  redata

    def cancelabcpay(self, orderId):
        """'快E付'退款"""
        # 说明 ： 快E付退款 支付成功 oms单号生产异常订单通过此接口退款
        # 入参证企订单号
        FuncName = self.cancelabcpay.__doc__
        data = StandConfig.Cancelabcpay.data
        appMethod = StandConfig.Cancelabcpay.method
        data = data % ({"orderId": orderId})
        sign = self.GetSign(self.appKey, self.appSecret, appMethod=appMethod, reqTime=self.nowtime, data=data)
        self.reqData.update({"appKey": self.appKey, "appMethod": appMethod, "reqParam": data,
                             "appRequestTime": self.nowtime, "signInfo": sign})
        resp = self.common.post(url=self.host, data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        print(data)
        redata = resp["apiTestResp"]
        print(redata)
        return redata

    def individualeinvoice(self,gcOrderNo,gcItemNo):
        """混合支付个人部分电子发票查询接口"""
        #说明：
        #gcOrderNo ： 政企订单号
        #gcItemNo  ： 证企订单行号
        #订单号、订单行号 二者必传其一 如果都传 以订单行为准
        FuncName = self.individualeinvoice.__doc__
        data = StandConfig.Individualeinvoice.data
        appMethod = StandConfig.Individualeinvoice.method
        data = data % ({"gcOrderNo": gcOrderNo,"gcItemNo":gcItemNo})
        sign = self.GetSign(self.appKey, self.appSecret, appMethod=appMethod, reqTime=self.nowtime, data=data)
        self.reqData.update({"appKey": self.appKey, "appMethod": appMethod, "reqParam": data,
                             "appRequestTime": self.nowtime, "signInfo": sign})
        resp = self.common.post(url=self.host, data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)
        return redata

    def addindividualeinvoice(self,znxbj,gcItemNo,companyName='',contractMobile='18312238756'):
        """混合支付个人部分电子发票申请接口"""
        #说明：
        #znxbj          ： 正逆向标识  1正向 -1逆向
        #gcItemNo       ： 证企订单行号
        #companyName    ： 个人电子发票开票抬头
        #contractMobile ： 11位手机号
        FuncName = self.addindividualeinvoice.__doc__
        data = StandConfig.Addindividualeinvoice.data
        appMethod = StandConfig.Addindividualeinvoice.method
        data = data % ({"znxbj": znxbj,"gcItemNo":gcItemNo})
        sign = self.GetSign(self.appKey, self.appSecret, appMethod=appMethod, reqTime=self.nowtime, data=data)
        self.reqData.update({"appKey": self.appKey, "appMethod": appMethod, "reqParam": data,
                             "appRequestTime": self.nowtime, "signInfo": sign})
        resp = self.common.post(url=self.host, data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        redata = resp["apiTestResp"]
        print(redata)
        return redata


    def mixOrder_Alipay(self,skuIds,isservFee,pay4237,companyCustNo="",nums='1',orderType=0,hopeArrivalTime='',\
                        isInvoice=1,payType="20",invoiceType=4,\
                    province="100",city="025",county="01",townId='99',address='南京玄武1'):
        """农行小豆创建订单接口"""
        #说明：下多个品时，skuIds="121347748,121347746",nums="1,2"
        #则121347748购买1个，121347746购买2个

        # companyCustNo: 子账号会员编码
        # orderType: 订单类型(0.实时型订单1.预占型订单)
        # isInvoice: 是否开发票(1 = 开，0 = 不开)
        # payType: 支付方式(20-混合支付)
        # invoiceType: 发票类型：1-增值税专票;2-普票（即卷票，票随货走）;
        #                       3-增值税普票（即平推式普票，票货分离）；4-电子发票

        FuncName = self.mixOrder_Alipay.__doc__

        tradeNo = "mixAlipay" + str(self.timestmp) + str(random.randint(1,1000))
        data = StandConfig.Mixpayorder_Alipay.data
        appMethod = StandConfig.Mixpayorder_Alipay.method
        skuInfo = ""
        amount = 0
        servFee = 0
        i=0
        sku = skuIds.split(",")

        for num in nums.split(','):
            priceInfo = self.getPrice(sku[i],city)
            price = list(priceInfo.values())[0]
            skuInfo = skuInfo + "<sku><num>%(num)s</num><skuId>%(sku)s</skuId>\
                <unitPrice>%(price)s</unitPrice></sku>" % ({"num": num, "sku": sku[i], "price": price})
            val = float(price) * int(num)
            amount = float('%.2f' % Decimal(amount)) + float('%.2f' % Decimal(val))
            amount = float('%.2f' %amount)
            i = i + 1

        if isservFee == 'Y':
            if amount < 86:
                servFee = 5
                Alamount = amount + servFee
            else:
                servFee = 0
                Alamount = amount + servFee

        pay4237 = pay4237
        pay9005 = float(Decimal(str(Alamount)) - Decimal(str(pay4237)))


        data = data % (
        {"province": province, "city": city, "county": county, "townId":townId,"address":address + tradeNo,"payTpye": payType, "orderType": orderType,
         "isInvoice": isInvoice, "invoiceType": invoiceType, "tradeNo": tradeNo, "companyCustNo": companyCustNo,"hopeArrivalTime":hopeArrivalTime,
         "servFee": servFee, "amount": float('%.2f' % Decimal(amount)), "skuInfo": skuInfo,"9005":pay9005,"4237":pay4237})
        sign=self.GetSign(self.appKey,self.appSecret,appMethod=appMethod,reqTime=self.nowtime,data=data)
        self.reqData.update({"appKey":self.appKey,"appMethod":appMethod,"reqParam":data,
                               "appRequestTime":self.nowtime,"signInfo":sign})
        resp = self.common.post(url=self.host,data=self.reqData, FuncName=FuncName, isLog=self.isLog)
        print(self.reqData)
        redata = resp["apiTestResp"]
        print(redata)

        return redata










