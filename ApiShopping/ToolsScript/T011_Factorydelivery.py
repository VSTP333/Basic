'''厂送确认收货接口'''

import requests
import uuid
import json
import bs4
import re
import time

class FactoryInte():
    def __init__(self):
        # 登录仓配一体
        uuid1 = uuid.uuid1()
        self.session = requests.session()
        url = "https://ssopre.cnsuning.com/ids/login"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                   "X-Requested-With": "XMLHttpRequest",
                   "Host": "somppre.cnsuning.com"}

        data = {
            "username": "15070441",
            "token": "",
            "service": "http://bsomppre.cnsuning.com/somp/auth?targetUrl=http%3A%2F%2Fbsomppre.cnsuning.com%2Fsomp%2FdeliveryErrMgr%2FtoDeliv.action",
            "uuid": uuid1,
            "loginTheme": "defaultTheme",
            "password2": "TiS+Kqm2rUrsJ+WU1oregOj2vxqqDkrCh7qjLQHYAO7IBEm9hIu3YmAPv+WH3sB6B/YW3wTi12gxiR2llHA5wJ6BMpoSY2E0VbhQ9p4rK8ghjU9fAeVsyayMO6WQEMZggiXKxMsF8URRIOU9AvlSq9ewhM+dje+U798T1ppNy9M="
        }
        self.session.post(url, data=data)

    def toDeliv(self,gc_order_no='',omsorderitemno=''):
        #查询订单
        url = "http://bsomppre.cnsuning.com/somp/deliveryErrMgr/toDeliv.action"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        if gc_order_no:
            data = {"b2cordercode": gc_order_no,
                    "shardname": "shard1"
                    }
        else:
            data = {"omsorderitemno": omsorderitemno,
                    "shardname": "shard1"
                    }


        ctime = 0
        while ctime != 600:
            req = self.session.post(url, data=data, headers=headers)
            soup = bs4.BeautifulSoup(req.content.decode("utf-8"), "lxml")
            rest = soup.find_all("a", class_="mr10 editProduction")
            regex_str = "[(](.*?)[)]"
            match_obj = re.findall(regex_str, str(rest))

            if match_obj:
                for i in range(len(match_obj)):
                    or_info = match_obj[i].strip("'").split("','")
                    if len(or_info)!=4:
                        print("errid未找到，请稍后" + str(ctime))
                        time.sleep(10)
                        ctime = ctime + 10

                    else:
                        self.modifyDeliveryFlag(or_info)
                        return 0
            else:
                print("订单未找到，请稍后" + str(ctime))
                time.sleep(10)
                ctime = ctime + 10

    def modifyDeliveryFlag(self,or_info):
        # 修改仓配一体类型
        url = "http://bsomppre.cnsuning.com/somp/deliveryErrMgr/modifyDeliveryFlag.action"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        errid = or_info[0]
        b2cOrderCode = or_info[1]
        omsOrderItemNo = or_info[2]
        suppliercode = or_info[3]
        data = {"errid": errid,
                 "b2cOrderCode": b2cOrderCode,
                 "suppliercode": suppliercode,
                 "omsOrderItemNo": omsOrderItemNo}
        ss = self.session.post(url, data=data, headers=headers)
        if ss.text=='{"errCode":0}':
            print(str(omsOrderItemNo)+'由仓配一体订单修改为普通厂送订单成功')

class FactorySend():
    def __init__(self,loginId):
        # 登录发货平台
        uuid1 = uuid.uuid1()
        self.session = requests.session()
        url = "https://mpassportpre.cnsuning.com/ids/login"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                   "X-Requested-With": "XMLHttpRequest",
                   "Host": "somppre.cnsuning.com"}

        if loginId=='A':
            username = "chenrpa@cnsuning.com"
            password2 = "FAlqjK8W3QRBVkCCkui7nwYCkW1R7SkmrGJUVDsB8mIMh0BY5HVaqUsIbseIqlIvD1gu5mp8HTvoQGWrcUqyRjnznVbXJs90iW5A+p/96aC1QqMoxULB3qfHJbpxTFEmQ6VmUCMsykjY7Er26fIr6YIJk9U6vFrcBFZaSEvkwNY=",
        if loginId=='B':
            username = "candasit01@126.com"
            password2 = "XC4Pfc8A3JRrKlVPqfrYlamhMh+zRZ4dt30LYYAg+QZM4x3OQDQSgGXZS3W6r0A4yeWbAK8c/UsCRhwUT+81h+ojZaUO/7cyE92WKZxSfYnVAXcOb13ZNTi5RMSGpDVcExOUM+rjxpoE0YCMY9lLHcYNdRmT6HitbOKdaQdtQfM="
        data = {
            "username": username,
            "password": "",
            "service": "http://mwspre.cnsuning.com/mws/auth?targetUrl=https%3A%2F%2Fmwspre.cnsuning.com%2Fmws%2FtradeCenter%2FshowMainTradeCenter.action",
            "uuid": uuid1,
            "loginTheme": "sop",
            "password2": password2,
            "verifyCode": "",
            "cpuId": "",
            "channel": "PC",
            "sysCodeNew": "SOP",
            "orderChannel": "208000103084",
            "detect": "",
            "dfpToken": "",
            "iarVerifyCode": ""
        }
        self.session.post(url, data=data)

    def querySaleOrders(self,gc_order_no):
        #使用政企订单号查询
        url = 'http://somppre.cnsuning.com/somp/saleOrder/querySaleOrders.action'
        data = {"b2cordercode":gc_order_no,
                "begindate":"",
                "enddate":"",
                "tabtype":"tab_6",
                "snXS":"0",
                "href":"/somp/saleOrder/saleOrderManage.action"}
        ctime=0
        while ctime!=600:

            req = self.session.post(url=url, data=data, headers=self.headers)
            soup = bs4.BeautifulSoup(req.content.decode("utf-8"), "lxml")
            rest=soup.find_all("p")

            regex_str = "<p>[\u4E00-\u9FA5]+</p>"
            match_obj = re.search(regex_str, str(rest))

            rest1 = soup.find_all("span")
            regex_str1 = "[发货]+"
            match_obj1 = re.search(regex_str1, str(rest1))

            if match_obj:
                order_status = match_obj.group(0)[3:-4]
                if order_status != "待发货":
                    print("当前订单状态为：" + order_status + "。不能发货")
                    exit()
                else:
                    regex_str = re.compile("销售订单行号.+")
                    oms_obj = regex_str.findall(str(rest))
                    regex_str = re.compile("仓配一体")
                    match_obj2 = regex_str.findall(str(rest))
                    if match_obj2:
                        if match_obj2[0] == "仓配一体":
                            if match_obj1.group(0)=="发货":
                                pass
                            else:
                                FactoryInte().toDeliv(gc_order_no=gc_order_no)
                    return oms_obj
            else:
                print("订单未找到，请稍后"+ str(ctime))
                time.sleep(10)
                ctime = ctime + 10


    def querySaleOmsNo(self,oms_item_no):
        #使用oms订单行号查询
        url = 'http://somppre.cnsuning.com/somp/saleOrder/querySaleOrders.action'
        data = {"omsorderitemno":oms_item_no,
                "begindate":"",
                "enddate":"",
                "tabtype":"tab_6",
                "snXS":"0",
                "href":"/somp/saleOrder/saleOrderManage.action"}
        ctime=0
        while ctime!=600:
            req = self.session.post(url=url, data=data, headers=self.headers)

            soup = bs4.BeautifulSoup(req.content.decode("utf-8"), "lxml")
            rest=soup.find_all("p")
            regex_str = "<p>[\u4E00-\u9FA5]+</p>"
            match_obj = re.search(regex_str, str(rest))
            rest1 = soup.find_all("span")
            regex_str1 = "<p>[\u4E00-\u9FA5]+</p>"
            match_obj1 = re.search(regex_str1, str(rest1))
            print(match_obj1)
            if match_obj:
                order_status = match_obj.group(0)[3:-4]
                if order_status not in ("待发货","部分发货"):
                    print("当前订单状态为：" + order_status + "。不能发货")
                    exit()
                else:
                    regex_str = re.compile("仓配一体")
                    match_obj2 = regex_str.findall(str(rest))
                    if match_obj2:
                        if match_obj2[0] == "仓配一体":
                            if match_obj1.group(0) == "发货":
                                pass
                            else:
                                FactoryInte().toDeliv(omsorderitemno=oms_item_no)
                    return 0
            else:
                print("订单未找到，请稍后"+ str(ctime))
                time.sleep(10)
                ctime = ctime + 10

    def cs_order(self,oms_no, mood):
        """
        order_no: 政企单号
        mood： 1为苏宁自营发货，2为第三方快递发货
        """
        # 发送发货请求
        url = "http://somppre.cnsuning.com/somp/orderDelivery/deliveryProcessOrder.action"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                   "X-Requested-With": "XMLHttpRequest",
                   "Host": "somppre.cnsuning.com"}
        order_no = ""
        k = 0

        if mood == '1':
            for i in oms_no:
                regex_str = re.compile("\d+")
                match_obj = regex_str.findall(str(i))
                if k!=0:
                    order_no = order_no + "," + match_obj[0] + "_"
                else:
                    order_no = match_obj[0] + "_"
                k = k + 1

            # 苏宁自配送请求报文
            data = {"checkOrder": order_no,
                    "mode": "SelfDistribution",
                    "isPageDelivery": "1",
                    "sendertel": "123123123",
                    "outercode": "13123213",
                    "sender": "啦啦"}

            print("苏宁自营发货")
        elif mood=='3':
            for i in oms_no:
                regex_str = re.compile("\d+")
                match_obj = regex_str.findall(str(i))
                if k!=0:
                    order_no = order_no + "," + match_obj[0] + "_3828743898704"
                else:
                    order_no = match_obj[0] + "_3828743898704"
                k = k + 1


            data = {"checkOrder": order_no,
                     "mode": "Third-party",
                     "isPageDelivery": "1",
                     "outercode": "3828743898704",
                     "companyCode": "SN2",
                     "companyName": "苏宁物流"}
            print("第三方快递发货")

        else:
            for i in oms_no:
                regex_str = re.compile("\d+")
                match_obj = regex_str.findall(str(i))
                if k!=0:
                    order_no = order_no + "," + match_obj[0] + "_3828743898704"
                    # order_no = order_no + "," + omsOrderItemNo + "_3828743898704"
                else:
                    order_no = match_obj[0] + "_3828743898704"
                    # order_no = omsOrderItemNo + "_3828743898704"
                k = k + 1


            data = {"checkOrder": order_no,
                     "mode": "Third-party",
                     "isPageDelivery": "1",
                     "outercode": "3828743898704",
                     "companyCode": "Y02",
                     "companyName": "韵达快运"}
            print("第三方快递发货")

        ss = self.session.post(url, data=data, headers=headers)

        if "RESTRICTED" in ss.text:
            print("登录失败，请重新获取password")
        else:
            print("发货结果：", json.loads(ss.text))
        return json.loads(ss.text)

    def cs_item(self,oms_no, mood):
        """
        oms_no: oms订单行号，一次只发一行
        mood： 1为苏宁自营发货，2为第三方快递发货
        """
        # 发送发货请求
        url = "http://somppre.cnsuning.com/somp/orderDelivery/deliveryProcessOrder.action"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                   "X-Requested-With": "XMLHttpRequest",
                   "Host": "somppre.cnsuning.com"}
        if mood == '1':
            # 苏宁自配送请求报文
            data = {"checkOrder": oms_no + "_",
                    "mode": "SelfDistribution",
                    "isPageDelivery": "1",
                    "sendertel": "123123123",
                    "outercode": "13123213",
                    "sender": "啦啦"}
            print("苏宁自营发货")
        else:
            data = {"checkOrder": oms_no + "_3828743898704",
                     "mode": "Third-party",
                     "isPageDelivery": "1",
                     "outercode": "3828743898704",
                     "companyCode": "Y02",
                     "companyName": "韵达快运"}
            print("第三方快递发货")
        ss = self.session.post(url, data=data, headers=headers)
        if "RESTRICTED" in ss.text:
            print("登录失败，请重新获取password")
        else:
            print("发货结果：", json.loads(ss.text))
        return json.loads(ss.text)


if __name__ == '__main__':
    """参数gc_orders：政企单号
       参数mood：1苏宁自发货、2韵达快递发货、3苏宁物流发货"""
    # A：chenrpa@cnsuning.com
    # B：candasit01@126.com

    loginId = 'A'
    fa = FactorySend(loginId)

    #政企订单号,会把订单下所有行都发货
    # gc_orders = '100002073154'
    # oms_no = fa.querySaleOrders(gc_order_no=gc_orders)
    # fa.cs_order(oms_no=oms_no, mood='2')


    #OMS订单行号,一次只发一行
    oms_items='00105641031002'
    fa.querySaleOmsNo(oms_item_no=oms_items)
    fa.cs_item(oms_no=oms_items, mood='3')