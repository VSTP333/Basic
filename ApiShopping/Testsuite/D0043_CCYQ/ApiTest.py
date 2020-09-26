#!/usr/bin/env python
# encoding: utf-8
'''
@author: 18056678（郭海龙）
@project: ApiShopping
@file: ApiTest.py
@time: 2019-12-24 17:43:42
@desc:
'''
from API.D0043_CCYQ.Base import API
api = API(envi='pre',user='HBYC',isLog='N')
skus = '102473734'
# 接收采购平台订单消息 = api.handMsg(business='ORDER',event='ADD',pcode='HB202005200006')
# 接收采购平台订单确认消息 = api.handMsg(business='ORDER',event='CONFIRM',pcode='HB202005200006',status=0)
# 接收采购平台订单取消消息 = api.handMsg(business='ORDER',event='CONFIRM',pcode='HB202004060004',status=1)
接收采购平台取消订单行消息 = api.handMsg(business='ORDER_ITEM',event='CANCEL',code='1',pcode='HB202004060004',itemCode='1',itemPcode='1')
# 接收采购商类目同步消息 = api.handMsg(business='GOODS_CATEGORY',event='SYNC',code='010203',level=3,name='三级类目名称',parentCode='0102',status=0)
# 接收采购商地址库同步消息 = api.handMsg(business='AREA',event='SYNC',lowCode='1300000000',newCode='',parentCode='1310000000',name='北戴河县',level=0,status=0)
# 接收采购平台收货单消息 = api.handMsg(business='RECEIVE',event='ADD',pcode='HB202005200003')
# 接收采购平台退货单消息 = api.handMsg(business='REFUND',event='ADD',pcode='2004010000003')
# 接收取消订单消息 = api.handMsg(business='ORDER',event='CANCEL',code='P2020331051')
# 接收对账单确认驳回消息 = api.handMsg(business='BILL',event='CONFIRM',code='2020033112345678',pcode='B0001',reason='驳回',status=1)
# 接收对账单结果消息_成功 = api.handMsg(business='BILL',event='RESULT',code='202005217018404598',itemCode='100002032865',status=0,billStatus=0,pBillCode='20200521100007')
# 接收对账单结果消息_失败 = api.handMsg(business='BILL',event='RESULT',code='202005217018404598',itemCode='100002032865',status=0,billStatus=1,pBillCode='20200521100009')
# 接收开票申请消息 = api.handMsg(business='INVOICE',event='ADD',pcode='EL202005201102')
# 接收发票确认驳回消息 = api.handMsg(business='INVOICE',event='CONFIRM',pcode='invoice0403001',status=1)
# 查询物流信息 = api.getLogistic(code='00105619179001')
# 获取价格及税率 = api.getProdPriceAndTaxcode(skus=skus,provinceCode='110000000000',citycode='110100000000',countyCode='110114000000')
# 校验商品售卖区域 = api.checkSalearea(skus=skus,provinceCode='110000000000',citycode='110100000000',countyCode='110114000000',townCode='110114003000')
# 获取商品上下架状态 = api.getShelvesStatus(skus=skus)
# 校验商品是否有库存 = api.getStockStatus(skus=skus,nums='30')