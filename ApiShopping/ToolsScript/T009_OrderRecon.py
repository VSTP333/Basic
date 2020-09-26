#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: T009_OrderRecon.py
@time: 2019-11-13 15:29:15
@desc:插入订单对账数据
'''
from Tools.mysql import MySql
import time

class OrderRecon():
    def __init__(self):
        self.mysql = MySql(envi='pre')
        pass

    def insertData(self,orderItemId='',create_time=''):


        sql = "update srcorder_item set status='06',create_time=DATE_FORMAT('{}','%Y-%m-%d %H:%i:%s'),update_time=DATE_FORMAT('{}','%Y-%m-%d %H:%i:%s')  where  gc_item_no='{}'".format(
            create_time, create_time, orderItemId)
        self.mysql.updates(sql)
        sql1 = "update srcorder_header set create_time=DATE_FORMAT('{}','%Y-%m-%d %H:%i:%s'),update_time=DATE_FORMAT('{}','%Y-%m-%d %H:%i:%s')  where  gc_order_no='{}'".format(
            create_time, create_time, orderItemId[0:-2])
        self.mysql.updates(sql1)

        id = str(time.strftime('%Y%m%d%H%M%S', time.localtime())) + str(int(time.time()*1000000))
        sql3="select order_no,oms_item_no,create_time,commdty_code,supplier_code,unit_price,quantiy,freight,cust_no from srcorder_item where  gc_item_no = '%s'" % orderItemId
        itemResult = self.mysql.searchs(sql3)

        gc_order_no = itemResult[0][0]    #政企订单号
        oms_item_no = itemResult[0][1]    #OMS订单行号
        oms_order_no = oms_item_no[0:-2]  # OMS订单号
        # create_time = itemResult[0][2]    #订单创建时间
        commdty_code = itemResult[0][3]   #商品编码
        supplier_code = itemResult[0][4]  #供应商编号
        unit_price = itemResult[0][5]     #单价
        quantiy = itemResult[0][6]        #数量
        total_freight = itemResult[0][7] #运费
        cust_no = itemResult[0][8]       #用户
        cart_two_no = 'mix15736981341648125'

        sqls = "select org_name,org_account,p_org_code from zs_org where org_code='%s'" % cust_no
        org_result = self.mysql.searchs(sqls=sqls)
        org_name = org_result[0][0]
        org_account = org_result[0][1]
        p_org_code = org_result[0][2]
        if p_org_code == '0':
            p_org_code = cust_no
            p_org_name = org_name
            p_org_account = org_account
        else:
            sqls = "select org_name,org_account from zs_org where org_code='%s'" % p_org_code
            p_org_result = self.mysql.searchs(sqls=sqls)
            p_org_name = p_org_result[0][0]
            p_org_account = p_org_result[0][1]

        table_num = int(p_org_code)%64

        sqls = "select table_num from gc_order_split_strategy_config where user_code='%s'" % p_org_code
        tableNum = self.mysql.searchs(sqls=sqls)

        if tableNum:
            sql = "update srcorder_item{} set status='06',create_time=DATE_FORMAT('{}','%Y-%m-%d %H:%i:%s'),update_time=DATE_FORMAT('{}','%Y-%m-%d %H:%i:%s')  where  gc_item_no='{}'".format(
                tableNum[0][0],create_time, create_time, orderItemId)
            self.mysql.updates(sql)
            sql1 = "update srcorder_header{} set create_time=DATE_FORMAT('{}','%Y-%m-%d %H:%i:%s'),update_time=DATE_FORMAT('{}','%Y-%m-%d %H:%i:%s')  where  gc_order_no='{}'".format(
                tableNum[0][0],create_time, create_time, orderItemId[0:-2])
            self.mysql.updates(sql1)

        sql = "INSERT INTO `gcmspre1`.`real_time_order_info%s`(`id`, `oms_order_no`, `gc_order_no`, `cart_two_no`, `gc_item_no`,\
         `oms_item_no`, `rtn_oms_item_no`, `status`, `is_refund_order`, `is_return`, `create_time`, `update_time`, `pay_time`,\
          `commdty_code`, `supplier_code`, `brand_name`, `first_category`, `second_category`, `third_category`, `commdty_name`,\
           `unit_price`, `quantiy`, `total_freight`, `total_amt`, `order_source`, `zs_order_source`, `pay_way`, `level`,\
            `balance_unit_account`, `balance_unit_name`, `balance_unit_code`, `purchase_unit_account`, `purchase_unit_name`, \
            `purchase_unit_code`, `linker_name`, `linker_mobile`, `prov_code`, `city_code`, `district_code`, `addr_detail`, \
            `invoice_type`, `invoice_title`, `invoice_status`, `first_puser_code`, `second_puser_code`, `third_puser_code`,\
             `online_pay_amount`, `company_pay_amount`, `storage_time`, `order_storage`, `package_number`,\
              `portion_return_count`, `po_no`, `promot_tax`, `external_order_no`, `invoice_remark`, `order_status`, \
              `operator_time`, `order_remark`, `user_nick_name`, `activity_main_id`, `activity_main_name`, `cost_center_user`, \
              `finish_time`) VALUES ('%s','%s','%s','%s','%s','%s', NULL, '4', 0, 2,'%s','%s','%s','%s','%s',NULL, NULL, NULL, NULL, NULL,%s,%s,%s,\
              15.000000, 'API', NULL, '08', 1,'%s','%s','%s','%s','%s','%s','品如', '15811109281', '江苏省', '南京市','玄武区', \
              '北清路68号用友软件园', 5, '品如', '2', '0', '0', '0', 0.000000,0.000000, NULL, '0', NULL, '0', NULL, 0.17, NULL, NULL,\
              '06','%s', NULL, '%s',NULL, NULL, NULL, NULL)"%(table_num,id,oms_order_no,gc_order_no,cart_two_no,orderItemId,\
              oms_item_no,create_time,create_time,create_time,commdty_code,supplier_code,unit_price,quantiy,total_freight,\
              p_org_account,p_org_name,p_org_code,org_account,org_name,cust_no,create_time,p_org_account)
        cc=self.mysql.inserts(sql)

if __name__ == '__main__':

    #暂时只为给平安健康客户写妥投对账信息用
    OrderRecon().insertData(orderItemId='10000181843301',create_time='2019-11-12 15:00:00')
