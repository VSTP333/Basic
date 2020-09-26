#!/usr/bin/env python
# encoding: utf-8
'''
@author: guohailong
@project: ApiShopping
@file: T002_PushMessage.py
@time: 2019-05-20 08:46:05
@desc: 手工造消息
'''

from Tools.mysql import MySql
from Tools.operatetool import Commontool
import time
import json


#往api_push_message表插入标准消息
class PushMessage(object):
    """
    往api_push_message表插入消息
    1.outing写入标准type 12 物流消息
    2.product写入标准type 10 商品消息
    3.Bill写入标准type 17 账单消息
    4.changePrice写入定制价格变动type 2 价格消息
    """
    def __init__(self):
        self.gcms_pre = MySql(envi='pre')
        self.times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.gcbi_pre = MySql(envi='pre', db='GCBI')
        self.common = Commontool(envi='pre')


    def outing(self,orderId=None,orderItemNo=None,types="out",ret_num=''):
        """
        手动写入出库和妥投的消息
        out/access/reject/return  对应状态出库/妥投/拒收/退货
        """

        if types=="out":
            status = '1'
            orderStatus = "05"
        elif types=="access":
            status = '2'
            orderStatus = "06"
        elif types=="reject":
            status = '3'
            orderStatus = "08"
        elif types=="return":
            status = '4'
            orderStatus = "08"

        res_code = 'ture'
        #获取分表号
        table = self.common.getTableNum(orderId=orderId, orderItemNo=orderItemNo)
        # print("订单分表是：" + "srcorder_item" + str(table))

        try:
            if orderId:
                result = self.gcms_pre.searchs("select commdty_code,gc_item_no,gc_order_no,quantiy,cust_no from srcorder_item%s where gc_order_no='%s'" % (table,orderId))
                if types=="access":
                    self.gcms_pre.updates("update srcorder_item%s set DELIVERY_OVER_TIME='%s' WHERE gc_order_no='%s'" % (table,self.times,orderId))
            else:
                result = self.gcms_pre.searchs("select commdty_code,gc_item_no,gc_order_no,quantiy,cust_no from srcorder_item%s where gc_item_no='%s'" % (table,orderItemNo))
                if types=="access":
                    self.gcms_pre.updates("update srcorder_item%s set DELIVERY_OVER_TIME='%s' WHERE gc_item_no='%s'" % (table,self.times,orderItemNo))
            for i in result:
                commdty_code = str(i[0])  #商品编码
                gc_item_no = str(i[1])    #政企订单行号
                gc_order_no = str(i[2])   #政企订单号
                sku_num = str(i[3])       #商品数量
                cust_no = str(i[4])       #会员编码
                self.gcms_pre.updates(sqls="update srcorder_item{} set status='{}' where gc_item_no='{}'".format(table,orderStatus,gc_item_no))

                if types=="return":
                    if ret_num=='':
                        return_num = sku_num
                    else:
                        return_num = ret_num
                    commdty_code = commdty_code.lstrip("0")
                    message = {"cmmdtyCode": commdty_code, "orderNo": gc_order_no, "status": status,
                               "orderItemNo": gc_item_no,"num":return_num}
                    message = json.dumps(message, separators=(',', ':'))
                else:
                    message = {"cmmdtyCode":commdty_code,"orderNo":gc_order_no,"status":status,"orderItemNo":gc_item_no}
                    message = json.dumps(message,separators=(',', ':'))

                # sqls = """INSERT INTO api_push_message (type,message,app_key,\
                #           create_time,update_time,order_no,order_item_no,\
                #           cmmdty_code,status,message_status) VALUES  %s""" %((('12',str(message),top_org_code,self.times, \
                #                                                                self.times,gc_order_no,gc_item_no,commdty_code,'1',status)),)
                # self.gcms_pre.inserts(sqls=sqls)

                # 写分表
                top_org_code = self.common.getCustNo(cust_no=cust_no)
                num = int(top_org_code) % 64
                # print("消息分表是：" + "gcapi_push_message" + str(num))
                sqls = """INSERT INTO gcapi_push_message%s (type,message,cust_no,\
                       create_time,update_time,gc_order_no,gc_item_no,\
                       cmmdty_code,status,supplier_code,message_status,message_source) VALUES  \
                       ('12','%s','%s','%s','%s','%s','%s','%s','1','X','%s','system')""" % \
                       (num, str(message), top_org_code, self.times, self.times, gc_order_no,gc_item_no,commdty_code, status)
                self.gcbi_pre.inserts(sqls=sqls)
                self.gcms_pre.updates(sqls="update invoice_merge_reissue_order_info{} set status='{}' where gc_item_no='{}'".format(num,orderStatus,gc_item_no))

                # if not t:
                #     result = self.gcms_pre.searchs(
                #         "select message,`status` from api_push_message where order_item_no='{}' order by update_time desc limit 1".format(
                #             gc_item_no))
                #     result = result[0]
                #     print('消息：%s  状态：%s' % (result[0], result[1]))
                # else:
                #     print(t)

                if types=="reject":
                    status = '4'
                    message = {"cmmdtyCode": commdty_code, "orderNo": gc_order_no, "status": status,
                               "orderItemNo": gc_item_no,"num":sku_num}
                    message = json.dumps(message, separators=(',', ':'))
                    #写主表
                    # sqls = """INSERT INTO api_push_message (type,message,app_key,\
                    #           create_time,update_time,order_no,order_item_no,\
                    #           cmmdty_code,status,message_status) VALUES  %s""" % (
                    # (('12', str(message), top_org_code, self.times, \
                    #   self.times, gc_order_no, gc_item_no, commdty_code, '1', status)),)
                    # self.gcms_pre.inserts(sqls=sqls)

                    #写分表
                    sqls = """INSERT INTO gcapi_push_message%s (type,message,cust_no,\
                           create_time,update_time,gc_order_no,gc_item_no,\
                           cmmdty_code,status,supplier_code,message_status,message_source) VALUES  \
                           ('12','%s','%s','%s','%s','%s','%s','%s','1','X','%s','system')""" % \
                           (num, str(message), top_org_code, self.times, self.times, gc_order_no,gc_item_no,commdty_code, status)
                    self.gcbi_pre.inserts(sqls=sqls)
                    status = '3'   #处理多行时，拒收状态重置
                    # if not t1:
                    #     result = self.gcms_pre.searchs(
                    #         "select message,`status` from api_push_message where order_item_no='{}' and message_status='{}' order by update_time desc limit 1".format(
                    #             gc_item_no,status))
                    #     result = result[0]
                    #     print('消息：%s  状态：%s' % (result[0], result[1]))
                    # else:
                    #     print(t1)
        except:
            res_code = 'false'
        return res_code


    def product(self,skuId=None,custNo=None,state=None):
        '''
        手工写商品消息
        # 上架1  下架2  添加0 删除4 修改3 主图6
        '''

        num = self.gcms_pre.searchs("select table_num from gc_product_pool_split_strategy_config  where user_code='{}'".format(custNo))[0][0]
        page_num = self.gcms_pre.searchs("select my_category_code from zs_prd_pool_single{} where org_id='{}' and partnumber like '%{}'".format(num,custNo,skuId))
        if state in '3,6':
            message = '{"cmmdtyCode":"%s","time":"%s","status":"%s","page_num":"%s"}' % (skuId, self.times, state, str(page_num[0][0]))
        else:
            message = '{"cmmdtyCode":"%s","status":"%s","page_num":"%s"}' % (skuId, state, str(page_num[0][0]))

        #写主表
        # sqls = """INSERT INTO api_push_message (type,message,app_key,\
        #                       create_time,update_time,order_no,order_item_no,\
        #                       cmmdty_code,status,message_status) VALUES  %s""" % ((('10', str(message), custNo, self.times, \
        #                                                                             self.times, 'X', 'X', '000000000'+skuId, '1',state)),)
        # self.gcms_pre.inserts(sqls=sqls)
        # print(sqls)

        #写分表
        num = int(custNo)%64
        sqls = """INSERT INTO gcapi_push_message%s (type,message,cust_no,\
                                      create_time,update_time,gc_order_no,gc_item_no,\
                                      cmmdty_code,status,supplier_code,message_status,message_source) VALUES  \
                                      ('10','%s','%s','%s','%s','X','X','%s','1','X','%s','system')""" % \
               (num, str(message), custNo, self.times,self.times, '000000000' + skuId, state)
        self.gcbi_pre.inserts(sqls=sqls)
        print(sqls)

    def Bill(self,account=None,custNo=None):
        """
        手工写账单消息
        :param account:会员账号
        :param custNo: 母账号会员编码
        """

        num = int(custNo) % 64
        message = '{"time":"%s","status":"1","pin":"%s","billid":"201905010030007378"}' % (self.times,account)
        #写主表
        # sqls = """INSERT INTO api_push_message (type,message,app_key,\
        #                       create_time,update_time,order_no,order_item_no,\
        #                       cmmdty_code,status) values %s""" %(('17',str(message),custNo,self.times,self.times,'X','X','X','1'),)
        # self.gcms_pre.inserts(sqls=sqls)
        # print(sqls)

        #写分表

        sqls = """INSERT INTO gcapi_push_message%s (type,message,cust_no,\
                                      create_time,update_time,gc_order_no,gc_item_no,\
                                      cmmdty_code,status,supplier_code,message_status,message_source) VALUES  \
                                      ('17','%s','%s','%s','%s','X','X','X','1','X','1','system')""" % \
               (num, str(message), custNo, self.times,self.times)
        self.gcbi_pre.inserts(sqls=sqls)
        print(sqls)

    def changePrice(self,skus="",custNo="",city=""):
        """
        手工写价格变动消息
        :param skus:商品编码
        :param custNo:母账号会员编码
        :param city:价格变动城市
        :return:
        """

        num = int(custNo) % 64
        sku = []
        for i in skus.split(','):

            message = '{"cmmdtyCode":"%s","time":"%s","cityId":"%s"}' % (i, self.times, city)
            # sqls = """INSERT INTO api_push_message(type,message,app_key,create_time,update_time,\
            #                 order_no,order_item_no,cmmdty_code,status,message_status) VALUES  %s""" % (('2',str(message),\
            #                                                     custNo,self.times,self.times,'X','X',i,'1','0'),)
            # self.gcms_pre.inserts(sqls=sqls)
            # print(sqls)

            # 写分表
            sqls = """INSERT INTO gcapi_push_message%s (type,message,cust_no,\
                                                  create_time,update_time,gc_order_no,gc_item_no,\
                                                  cmmdty_code,status,supplier_code,message_status,message_source) VALUES  \
                                                  ('2','%s','%s','%s','%s','X','X','X','1','X','1','system')""" % \
                   (num, str(message), custNo, self.times, self.times)
            self.gcbi_pre.inserts(sqls=sqls)
            print(sqls)

    def invoiceMsg(self,orderId='',orderItemId='',markId='',invoiceType='1',status='2',invoiceSign='1',custNo=''):
        """
        手动写发票消息
        :param orderId: 政企订单号
        :param orderItemId: 政企订单行号
        :param markId: 发票markId
        :param invoiceType: 发票类型 1-增票 3-普票 4-电子发票
        :param status: 发票状态 2-开票 3-邮寄 4-妥投
        :param invoiceSign: 发票标识 1：蓝票  -1：红票
        :return: null
        说明：markId不为空时，orderId和orderItemId为空
        """
        num = int(custNo) % 64
        if markId != '': # {"markId":"zzspq0007test","invoiceSign":"1","invoiceType":"3","status":"3"}
            msg = '{"markId":"%s","invoiceSign":"%s","invoiceType":"%s","status":"%s"}' % (markId,invoiceSign,invoiceType,status)

        elif markId == '': # {"orderNo":"100001565566","invoiceSign":"1","orderItemNo":"10000156556601","invoiceType":"4","status":"2"}
            if orderId != '' and orderItemId == '':
                # 需要遍历订单行表，取出所有订单行号
                result = self.gcms_pre.searchs(sqls="SELECT gc_item_no from srcorder_item WHERE gc_order_no='%s'" %(orderId))
                for i in result:
                    msg = '{"orderNo":"%s","invoiceSign":"%s","orderItemNo":"%s","invoiceType":"%s","status":"%s"}' % \
                          (orderId,invoiceSign,i[0],invoiceType,status)
                    # print(msg)
                    # sqls = """INSERT INTO api_push_message ( type, message, app_key, create_time, update_time,  status,  message_status)
                    #                    VALUES %s""" % (('20', str(msg), custNo, self.times, self.times, '1', status),)
                    # # print(sqls)
                    # self.gcms_pre.inserts(sqls=sqls)
                    sqls = """INSERT INTO gcapi_push_message%s (type,message,cust_no,\
                                                          create_time,update_time,gc_order_no,gc_item_no,\
                                                          cmmdty_code,status,supplier_code,message_status,message_source) VALUES  \
                                                          ('20','%s','%s','%s','%s','X','X','X','1','X','%s','system')""" % \
                                                             (num, str(msg), custNo, self.times, self.times,status)
                    self.gcbi_pre.inserts(sqls=sqls)
            elif orderId == '' and orderItemId != '':
                orderId = orderItemId[0:-2]
                msg = '{"orderNo":"%s","invoiceSign":"%s","orderItemNo":"%s","invoiceType":"%s","status":"%s"}' % \
                    (orderId, invoiceSign, orderItemId, invoiceType, status)
                # print(msg)
            elif orderId != '' and orderItemId !='':
                orderId = orderItemId[0:-2]
                msg = '{"orderNo":"%s","invoiceSign":"%s","orderItemNo":"%s","invoiceType":"%s","status":"%s"}' % \
                      (orderId, invoiceSign, orderItemId, invoiceType, status)
            else:
                print("至少要输入一个吧？")

        # sqls = """INSERT INTO api_push_message ( type, message, app_key, create_time, update_time,  status,  message_status)
        #            VALUES %s""" % (('20',str(msg),custNo,self.times,self.times,'1',status),)
        # # print(sqls)
        # self.gcms_pre.inserts(sqls=sqls)

        # 写分表
        sqls = """INSERT INTO gcapi_push_message%s (type,message,cust_no,\
                                                          create_time,update_time,gc_order_no,gc_item_no,\
                                                          cmmdty_code,status,supplier_code,message_status,message_source) VALUES  \
                                                          ('20','%s','%s','%s','%s','X','X','X','1','X','%s','system')""" % \
               (num, str(msg), custNo, self.times, self.times,status)
        self.gcbi_pre.inserts(sqls=sqls)
        print(sqls)


if __name__ == '__main__':
    #标准物流消息type=12  out/access/reject/return  对应状态出库/妥投/拒收/退货
    #说明   ret_num为退货数量，全退留空，部分退需填具体数量

    # PushMessage().outing(orderId="100002073404",types="out",ret_num='')              #按单号
    # PushMessage().outing(orderItemNo='10000207313902',types='out',ret_num='')      #按行号
    # PushMessage().outing(orderItemNo='10000207300801',types='return',ret_num='')      #按行号
    #

    # 标准商品消息type=10 上架1  下架2  添加0  删除4  修改3  主图6
    # PushMessage().product(skuId='121347884', custNo='7018886010', state='6')
    # PushMessage().product(skuId='121347657', custNo='7018886010', state='6')
    # PushMessage().product(skuId='121347653', custNo='7018886010', state='6')
    # PushMessage().product(skuId='121347746', custNo='7018886010', state='6')
    # sku = 121347657
    # for i in range(510):
    #     PushMessage().product(skuId='121347644',custNo='7017966447',state='1')
        # sku = sku + 1


    #标准账单消息type=17
    # PushMessage().Bill(account='bsbank@126.com', custNo='7018416245')

    #定制价格变更消息
    # PushMessage().changePrice(skus='121347744,121347740',custNo='7018006552',city='025')
    # 发票消息
    PushMessage().invoiceMsg(custNo='7018166120',markId='FS2020070110646051',invoiceType='1',status='2')
    PushMessage().invoiceMsg(custNo='7018166120',markId='FS2020070110646051',invoiceType='1',status='3')
    PushMessage().invoiceMsg(custNo='7018166120',markId='FS2020070110646051',invoiceType='1',status='4')
    PushMessage().invoiceMsg(custNo='7018166120',markId='FS2020070110646318',invoiceType='1',status='2')
    PushMessage().invoiceMsg(custNo='7018166120',markId='FS2020070110646318',invoiceType='1',status='3')
    PushMessage().invoiceMsg(custNo='7018166120',markId='FS2020070110646318',invoiceType='1',status='4')



