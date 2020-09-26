#!/usr/bin/env python
# encoding: utf-8
'''
@author: guohailong
@project: ApiShopping
@file: T004_ReturnPart.py
@time: 2019-05-20 08:46:05
@desc:目前只支持无运费和运费能被除尽的场景（小数点后两位）
'''
from Tools.mysql import MySql
import time,json
from Tools.operatetool import Commontool

class ReturnPart():
    def __init__(self):
        self.mysql = MySql(envi='pre')
        self.times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.gcbi_pre = MySql(envi='pre', db='GCBI')
        self.common = Commontool(envi='pre')


    def fetchData(self,orderItemId):

        tn = self.common.getTableNum(orderItemNo=orderItemId)
        itemResult = self.mysql.searchs("select gc_order_no,oms_item_no,commdty_code,quantiy,unit_price,freight,order_header_no,cust_no,order_item_no,return_goods_num from srcorder_item%s where  gc_item_no = '%s'" % (tn,  orderItemId))
        gc_order_no = orderItemId[:-2]
        headerResult = self.mysql.searchs("select oms_order_no from srcorder_header%s where gc_order_no = '%s'" % (tn, gc_order_no))
        oms_order_no = str(headerResult[0])
        for i in itemResult:
            #gc_order_no = str(i[0])
            oms_item_no = str(i[1])
            commdty_code = str(i[2])
            quantiy = str(i[3])
            unit_price = str(i[4])
            freight = str(i[5])
            order_header_no = str(i[6])
            cust_no = str(i[7])
            order_item_no = str(i[8])
            return_goods_num = str(i[9])
            top_org_code = self.common.getCustNo(cust_no=cust_no)

            rtn_oms_item_no = str(int(time.time())) + '00001'
        # ('100001816649', '00102588006001', '000000000121347740', '5', '1000.000000', '0.000000', '1640000000000350510', '7018048617', '201809171245243362', '7018048617', '157337332800001', '1')
        return gc_order_no,oms_item_no,commdty_code,quantiy,unit_price,freight,order_header_no,cust_no,order_item_no,top_org_code,rtn_oms_item_no,return_goods_num

    # 检查退货数量
    def checkNum(self,orderItemId=''):
        gc_order_no = orderItemId[:-2]
        sqls = "select max(portion_return_num) from srcorder_item_portion_return where gc_item_no ='%s'" % orderItemId
        returnedNum = self.mysql.searchs(sqls=sqls)[0][0]
        if returnedNum is None:
            returnedNum = 0
        quantity = self.fetchData(orderItemId=orderItemId)[3]
        if returnedNum >= int(quantity):
            return True # 已退完
        else:
            return int(returnedNum)  # 未退完，则返回已退数量

    # 查询退货次数
    def checkCount(self,orderItemId=''):
        sqls = "select max(portion_return_count) from srcorder_item_portion_return where gc_item_no = '%s'" % orderItemId
        returnCount = self.mysql.searchs(sqls=sqls)[0][0]
        if returnCount is None:
            return int(0)
        else:
            return int(returnCount)

    # 退货商品分摊运费
    def servFeePerNum(self,orderItemId='',num=0):
        total_freight = self.fetchData(orderItemId=orderItemId)[5]
        quantity = self.fetchData(orderItemId=orderItemId)[3]
        perNum = float(total_freight) / int(quantity)
        return round(perNum*int(num),2)

    def insertData(self,orderItemId='',returnNum=''):
        gc_order_no = orderItemId[:-2]
        quantity = self.fetchData(orderItemId=orderItemId)[3]   #订单行商品总数量
        returnedNum = self.checkNum(orderItemId=orderItemId)  #已退数量

        cc = self.checkCount(orderItemId=orderItemId)   #已退次数
        oms_item_no = self.fetchData(orderItemId=orderItemId)[1]
        unit_price = self.fetchData(orderItemId=orderItemId)[4]

        cust_no = self.fetchData(orderItemId=orderItemId)[7]

        table_num = self.common.getTableNum(orderItemNo=orderItemId)
        top_cust_no = self.fetchData(orderItemId=orderItemId)[9]
        table_num_msg = int(top_cust_no)%64
        unit_price = "%.2f"%(float(unit_price))        #商品单价
        total_freight = self.fetchData(orderItemId=orderItemId)[5]  #订单行分摊运费
        portion_return_count = cc + 1 # 退货次数 = 已退货次数 + 1
        rtn_oms_item_no = str(int(time.time())) + '00001'
        if isinstance(returnedNum,bool) or cc >= 3:
            print("此订单已退完，无须再退")
        else:
            if (int(returnedNum) + int(returnNum))>=int(quantity) or portion_return_count == 3:  #全部退
                portion_return_price = int(quantity) * float(unit_price) + float(total_freight)  # 总退货金额
                returnNum = int(quantity) - int(returnedNum)   #本次退货数量
                print("本次退货数量returnNum为："+str(returnNum))
                reNum = quantity  #总退货数量
                servFee = self.servFeePerNum(orderItemId=orderItemId,num=int(returnedNum))  # 退货商品分摊运费
                current_rtn_freight = float(total_freight) - float(servFee)  # 本次退运费金额
                current_return_price = returnNum * float(unit_price) + current_rtn_freight  # 本次退货金额（含运费）
                status = '08'
            else: #部分退
                servFee = self.servFeePerNum(orderItemId=orderItemId, num=(int(returnedNum) + int(returnNum)))  # 退货商品分摊运费
                portion_return_price = (int(returnedNum) + int(returnNum)) * float(unit_price) + float(servFee)  # 总退货金额
                current_rtn_freight = int(returnNum) * float(servFee)  # 本次退运费金额
                reNum = int(returnedNum) + int(returnNum)  # 总退货数量
                cuservFee = self.servFeePerNum(orderItemId=orderItemId, num=int(returnNum))
                current_return_price = int(returnNum) * float(unit_price) + float(cuservFee)   # 本次退货金额（含运费）
                status = '06'

            up_sql = "update srcorder_item set status = '%s',portion_return_status = '1',return_goods_num = '%s' WHERE gc_item_no = '%s'" % (status, reNum, orderItemId)
            self.mysql.updates(sqls=up_sql)
            if table_num:
                # table_num = list(table_num)[0][0]
                up_sql4 = "update srcorder_item%s set status = '%s',portion_return_status = '1',return_goods_num = '%s' WHERE gc_item_no = '%s'" % (table_num, status, reNum, orderItemId)
                self.mysql.updates(sqls=up_sql4)
            in_sql = "insert into srcorder_item_portion_return (`gc_order_no`,`gc_item_no`,`oms_item_no`," \
                     "`portion_return_num`,`portion_return_count`,`portion_return_price`,`oms_opreate_time`," \
                     "`update_time`,`create_time`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                     % (
                     gc_order_no, orderItemId, oms_item_no, reNum, portion_return_count, round(portion_return_price,2),
                     self.times, self.times, self.times)
            up_sql2 = "update srcorder_item_portion_return set portion_return_num = '%s' , portion_return_count = '%s' " \
                      ", portion_return_price = '%s' , update_time = '%s' WHERE  gc_item_no = '%s'" \
                      % (reNum, portion_return_count, round(portion_return_price,2), self.times, orderItemId)
            if cc == 0:  # 如果没有发生过部分退，就insert
                self.mysql.inserts(sqls=in_sql)
            else:  # 如果发生过部分退，则update
                self.mysql.updates(sqls=up_sql2)
            # 向srcorder_item_portion_return_detail表中插入数据，以供售后进度查询使用
            in_sql2 = "insert into srcorder_item_portion_return_detail (`gc_order_no`,`gc_item_no`,`oms_item_no`," \
                      "`order_status`,`current_return_num`,`total_return_num`,`rtn_oms_item_no`,`rtn_price`,`rtn_freight`," \
                      "`oms_opreate_time`,`update_time`,`create_time`,`invoice_status`,`invoice_apply_date`,`cust_no`,`top_cust_no`)" \
                      " VALUES ('%s','%s','%s','06','%s','%s','%s','%s','%s','%s','%s','%s','0',NULL ,'%s','%s')" % \
                      (gc_order_no, orderItemId, oms_item_no,int(returnNum), reNum, rtn_oms_item_no, round(current_return_price,2),
                       round(current_rtn_freight,2),
                       self.times, self.times, self.times, cust_no, top_cust_no)
            # 2020/4/7日新增 退货时产生12-4消息
            message_status = '4'
            commdty_code = self.fetchData(orderItemId=orderItemId)[2]
            commdty_code = str(int(commdty_code))
            message = {"cmmdtyCode":commdty_code,"orderNo":gc_order_no,"status":message_status,"orderItemNo":orderItemId,"num":returnNum}
            message = json.dumps(message, separators=(',', ':'))
            in_sql3 = "insert into gcapi_push_message%s (type,message,cust_no,\
                                                      create_time,update_time,gc_order_no,gc_item_no,\
                                                      cmmdty_code,status,supplier_code,message_status,message_source) VALUES  \
                                                      ('12','%s','%s','%s','%s','%s','%s','%s','1','X','%s','system')""" % \
                       (table_num_msg, str(message), top_cust_no, self.times, self.times, gc_order_no,orderItemId,commdty_code, message_status)
            self.mysql.inserts(in_sql2)
            self.gcbi_pre.inserts(in_sql3)


if __name__ == "__main__":
    rt = ReturnPart()

    orderItemId = '10000206640004'   #政企订单行号

    returnNum  = '1'   #部分退数量

    rt.insertData(orderItemId,returnNum)

