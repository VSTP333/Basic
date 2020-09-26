#!/usr/bin/env python
# encoding: utf-8
'''
@author: guohailong
@project: ApiShopping
@file: T001_BillingInfo.py
@time: 2019-05-20 08:46:05
@desc: 手动写账单信息
'''

from Tools.mysql import MySql
import time
import datetime

gcms_pre = MySql(envi='pre')
gcbi_pre = MySql(envi='pre', db='GCBI')
times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
id = int(time.time() * 100000)


def getCustNo(cust_no=''):
    sqls = "select p_org_code from zs_org WHERE org_code = '%s'" % cust_no
    top_cust_no = gcms_pre.searchs(sqls=sqls)[0][0]
    if top_cust_no == '0':
        top_cust_no = cust_no
    return top_cust_no

def orderItemAccount(orderItemCode=None):
    """
    说明：手动写账单信息
    :param orderItemCode: 政企订单行号
    :param status: 状态
    :param orderCode: 政企订单号
    :return:
    """
    update_time_o = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    gcms_pre.updates("update srcorder_item set update_time = '%s',status = '06' WHERE gc_item_no = '%s'" % (update_time_o,orderItemCode))
    result_item = gcms_pre.searchs("select oms_item_no,gc_order_no,unit_price,quantiy,cust_no,freight,create_time,update_time,return_goods_num from srcorder_item where gc_item_no='%s'" % orderItemCode)
    oms_item_no = result_item[0][0]     # oms行号
    gc_order_no = result_item[0][1]     # 政企订单号
    unit_price = result_item[0][2]      # 商品单价
    quantity = result_item[0][3]         # 购买数量
    cust_no = result_item[0][4]         # 下单会员编码
    freight = result_item[0][5]         # 运费
    create_time = str(result_item[0][6])[0:9]     # 订单创建时间
    update_time_o = str(result_item[0][7])[0:9]   # 订单更新时间
    return_goods_num = result_item[0][8]  #部分退数量
    # 向zs_bill_base_info插入的数据
    p_org_code = getCustNo(cust_no=cust_no)  #母会员编号

    bill_cust_no = gcms_pre.searchs("select cust_no from gc_user_info where yg_cust_no = '%s'" % p_org_code)
    bill_cust_no = bill_cust_no[0][0] # 30客编

    billNo = str(time.strftime('%Y%m%d', time.localtime())) + str(bill_cust_no) # 账单编码
    day = (datetime.date.today())
    begin_Date = (day - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    create_Date = begin_Date
    pay_Date = (day + datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    total_Fee,sale_Fee,arr_Fee,change_Fee,bill_Interest = 880000.00,123.00,30000.00,800.00,0.00

    # 向zs_bill_detail_info插入的数据
    p_Price =  "%.2f" % (float(unit_price * quantity + freight))
    p_Order = gc_order_no
    payment_Status = '1'
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # 向gc_bill_order_info插入数据
    bill_no = billNo
    order_no = gc_order_no
    perNum = "%.2f" % (float(freight)/int(quantity))   #每个品分摊运费

    if return_goods_num:  #部分退
        servFee = round(float(perNum) * int(return_goods_num), 2)  # 退货商品分摊运费
        p_Price = float(p_Price) - int(return_goods_num) * float(unit_price) - float(servFee)  # 账单金额
        p_Price = "%.2f" % (p_Price)

    # 向base_info插数据
    base_result = gcms_pre.searchs("select 1 from zs_bill_base_info WHERE billNo = '%s'" % billNo)
    if not base_result:
        sqls = "INSERT INTO `zs_bill_base_info` ( `billNo`, `supplier_Code`, `begin_Date`, `end_Date`,\
                    `create_Date`, `pay_Date`, `total_Fee`, `sale_Fee`, `arr_Fee`, `change_Fee`, `bill_Interest`,\
                     `remark`) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '')"
        gcms_pre.inserts(sqls=sqls %(billNo,bill_cust_no,begin_Date,day,create_Date,pay_Date,total_Fee,sale_Fee,arr_Fee,change_Fee,bill_Interest))
    else:
        pass
    # 向detail_info插数据
    detail_result = gcms_pre.searchs("select 1 from zs_bill_detail_info WHERE p_OmsOrder = '%s' " % oms_item_no)
    if not detail_result:
        sqls = "INSERT INTO `gcmspre1`.`zs_bill_detail_info` ( `p_OmsOrder`, `old_OmsOrder`, `billNo`, `type`,\
              `p_Date`, `op_Date`, `p_Price`, `p_Order`, `remark`, `payment_Status`, `soa_Num`, `process_id`,\
               `opt_Account`, `error_message`, `batch_no`, `update_time`) VALUES ( '%s', NULL, '%s', '1', '%s',\
                '%s', '%s', '%s', '123', '%s', NULL, NULL, NULL, NULL, NULL, '%s')"
        gcms_pre.inserts(sqls=sqls % (oms_item_no,billNo,pay_Date,pay_Date,p_Price,p_Order,payment_Status,update_time))
    else:
        sqls = "UPDATE `gcmspre1`.`zs_bill_detail_info` SET  `old_OmsOrder`=NULL, `billNo`='%s', `type`='1',\
                `p_Date`='%s', `op_Date`='%s', `p_Price`='%s', `p_Order`='%s', `remark`='123', \
                `payment_Status`='%s', `soa_Num`=NULL, `process_id`=NULL, `opt_Account`=NULL,\
                 `error_message`=NULL, `batch_no`=NULL, `update_time`='%s' WHERE p_OmsOrder = '%s'"
        gcms_pre.updates(sqls=sqls % (billNo,pay_Date,pay_Date,p_Price,p_Order,payment_Status,update_time,oms_item_no))

    # 向gc_bill_order_info插数据
    order_result = gcms_pre.searchs("select 1 from gc_bill_order_info WHERE  order_no = '%s'" % order_no)
    if not order_result:
        sqls = "INSERT INTO `gc_bill_order_info` ( `bill_no`, `order_no`, `order_price`, \
            `order_cDate`, `order_fDate`, `create_time`, `update_time`) VALUES \
            ( '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        gcms_pre.inserts(sqls=sqls % (bill_no,gc_order_no,str(p_Price),create_time,update_time_o,update_time,update_time))
    else:
        # 如果表中数据不为空，先取到原字段的order_price，然后做累加
        old_price = gcms_pre.searchs("select order_price from gc_bill_order_info WHERE  order_no = '%s'" % order_no)
        old_price = old_price[0][0]
        sqls = "UPDATE `gc_bill_order_info` SET `bill_no`='%s',  `order_price`='%s', `order_status`='06',\
              `order_cDate`='%s', `order_fDate`='%s', `create_time`='%s', `update_time`='%s' WHERE order_no = '%s'"
        gcms_pre.updates(sqls=sqls % (bill_no,str(float(p_Price) + float(old_price)),create_time,update_time_o,update_time,update_time,gc_order_no))

    # 向api_push_message表中插数据
    message_result = gcms_pre.searchs("select 1 from api_push_message WHERE message like '%%%s%%' AND app_key = '%s'" % (bill_no,p_org_code))
    pin = gcms_pre.searchs("select user_account from zs_user WHERE  user_code = '%s'" % p_org_code)
    pin = pin[0][0]
    num = int(p_org_code) % 64
    if not message_result:
        message = '{"time":"%s","status":"1","pin":"%s","billid":"%s"}' % (times, pin,bill_no)
        sqls = """INSERT INTO api_push_message (type,message,app_key,\
                                  create_time,update_time,order_no,order_item_no,\
                                  cmmdty_code,status) values %s""" % (
            ('17', str(message), cust_no, times, times, 'X', 'X', 'X', '1'),)
        gcms_pre.inserts(sqls=sqls)

        # 写分表

        sqls = """INSERT INTO gcapi_push_message%s (type,message,cust_no,\
                                                                  create_time,update_time,gc_order_no,gc_item_no,\
                                                                  cmmdty_code,status,supplier_code,message_status,message_source) VALUES  \
                                                                  ('17','%s','%s','%s','%s','X','X','X','1','X','1','system')""" % \
               (num, str(message), p_org_code, times, times)
        gcbi_pre.inserts(sqls=sqls)
        print(sqls)
    else:
        gcms_pre.updates(sqls="update `api_push_message` set `status` = '1' WHERE `message` like '%%%s%%' AND `app_key` = '%s'" % (bill_no, p_org_code))

        gcbi_pre.updates(sqls="update gcapi_push_message%s set `status` = '1' WHERE `message` like '%%%s%%' AND `app_key` = '%s'" % (num,bill_no, p_org_code))


if __name__ == '__main__':

    orderItemAccount(orderItemCode='10000182551806')
