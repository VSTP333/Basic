#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: tools.py
@time: 2019-05-09 11:44:57
@desc:工具包,提供接口post请求方法等
'''

import time
import json,requests
import logging
from urllib import parse
from decimal import Decimal
import base64
import os
from Tools.mysql import MySql
from Tools.md5 import Md5
import winreg
from ToolsScript.T002_PushMessge import PushMessage
import re
from  Tools.operatetool import Commontool
class Common():

    def __init__(self,envi):
        self.mysql = MySql(envi)
        self.envi = envi
        self.dirname = os.path.join(os.getcwd(),"log")
        self.nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.common = Commontool(envi=envi)

    def getToken(self,appKey,token):
        """判断token是否过期"""
        result = self.mysql.searchs("select token,expire_date from api_token where api_account='{}'".format(appKey))
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if result:
            if str(result[0][1]) > nowtime:
                token = result[0][0]
            else:
                token = token()
        else:
            token = token()
        return token

    def getToken2(self,appKey):
        """不判断token是否过期"""
        result = self.mysql.searchs("select token,expire_date from api_token where api_account='{}'".format(appKey))
        if result:
            token = result[0][0]
        return token

    def scHost(self):
        """天线测试环境"""
        if str(self.envi)=="pre":
            return "http://txapipre.cnsuning.com"
        elif str(self.envi)=="sit":
            return "http://txapisit.cnsuning.com"
        elif str(self.envi)=="xgpre":
            return "http://txapixgpre.cnsuning.com"
        elif str(self.envi) == "prd":
            return "http://txapi.suning.com"

    def scHost_bz(self):
        """标准环境"""
        if str(self.envi)=="pre":
            return "http://openpre.cnsuning.com/ospos/apipage/testApiMethodInvoke.do"
        elif str(self.envi)=="sit":
            return "http://opensit.cnsuning.com/ospos/apipage/testApiMethodInvoke.do"
        elif str(self.envi)=="xgpre":
            return "http://openxgpre.cnsuning.com/ospos/apipage/testApiMethodInvoke.do"
        elif str(self.envi)=="online":
            return "https://open.suning.com/ospos/apipage/testApiMethodInvoke.do"


    def post(self,url=None,data=None,headers={},FuncName=None,isJson='N',isLog='Y',isReturnJson='N',isUrlEncode='N',isText='N'):
        "初始化HTTP请求的Header和Data"
        #isUrlEncode='N'时，请求data会进行url编码
        if isText=='N':
            if isLog=="Y":
                logger = str(FuncName) + "--" + "入参：" + str(json.dumps(data,ensure_ascii=False,separators=(',',':')))
                self.loger(info=logger)
            if isJson=='N':
                if headers == {}:
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                if isUrlEncode=='N':
                    data = parse.urlencode(data).encode("utf-8")
                else:
                    data = parse.urlencode(data)
                    data = (parse.unquote(data)).encode('utf-8')
            else:
                if headers == {}:
                    headers = {'Content-Type': 'application/json'}
                data = json.dumps(data)
        else:
            if isLog=="Y":
                logger = str(FuncName) + "--" + "入参：" + str(data)
                self.loger(info=logger)
            if headers == {}:
                headers = {'Content-Type': 'application/text/xml'}
        try:
            req = requests.post(url=url, headers=headers, data=data)

            if isLog == "Y":
                logger = str(FuncName) + "--" + "出参：" + str(req.text)
                self.loger(info=logger)
        except Exception as e:
            if isLog == "Y":
                logger = str(FuncName) + "--" + str(e)
                self.loger(error=logger)
            raise e

        ##增加判断是否返回json 2019.05.17

        if isReturnJson=='N':
            try:
                redata = json.loads(req.text)
            except:
                redata = req.text

        else:
            redata = req.text

        return redata

    def loger(self,info="",error=""):
        """打印日志"""
        nowtimes = time.strftime("%Y-%m-%d", time.localtime())
        logger = logging.getLogger(__name__)

        if os.path.exists(self.dirname):
            pass
        else:
            os.makedirs(self.dirname)

        handler = logging.FileHandler(os.path.join(self.dirname,str(nowtimes) + '.txt'))
        # handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if error=="":
            logger.setLevel(level=logging.INFO)
            logger.info(info)
        else:
            logger.setLevel(level=logging.ERROR)
            logger.error(error)
        logger.removeHandler(handler)

    def getInvoicePice(self,itemNo,isRe='N'):
        table = self.common.getTableNum(orderItemNo=itemNo)
        result = self.mysql.searchs("SELECT unit_price,quantiy FROM srcorder_item{} WHERE gc_item_no in ({})".format(table,itemNo))

        amount=0
        for k in result:
            price = k[0]
            num = k[1]
            val = float(price) * int(num)
            amount = float('%.2f' % Decimal(amount)) + float('%.2f' % Decimal(val))

        if isRe=='Y':
            result = self.mysql.searchs(
                "select portion_return_price from srcorder_item_portion_return where gc_item_no in ({})".format(itemNo))
            for i in result:
                return_price = i[0]
                amount = float('%.2f' % Decimal(amount)) - float('%.2f' % Decimal(return_price))
        return amount

    def getSign(self,appKey = None, appSecret = None, appMethod = None, reqTime = None, version = "v1.2", data = None):
        """
         接口说明：生成标准3.0接口验签
         :param appKey: appkey
         :param appSecret: secret
         :param appMethod: 接口调用方法
         :param reqTime: 调用接口时间
         :param version: 开放平台接口版本
         :param data: 接口请求报文
         :return: 返回生成的验签
         """
        md5 = Md5()
        dataBase64 = str(base64.b64encode(data.encode('utf-8')), encoding="utf-8")
        sign = appSecret + appMethod + reqTime + appKey + version + dataBase64
        md5_text = md5.getMd5_32(text=sign)

        return md5_text

    def getSecret(self,appKey):
        """获取定制用户appSecret"""
        result = self.mysql.searchs("select api_secret from gc_secret where api_account='{}'".format(appKey))
        return result[0][0]

    def updatOrderStatus(self,orderId='',orderItemNo='',types=''):
        """更改订单状态并写标准消息"""
        #types: out/access/reject/return  对应状态出库/妥投/拒收/退货
        result = PushMessage().outing(orderId=orderId,orderItemNo=orderItemNo,types=types)
        return result


    def get_desktop(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]

    def loads_jsonp(self, _jsonp):
        """
        解析jsonp数据格式为json
        :return:
        """
        try:
            return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
        except:
            print(_jsonp)




