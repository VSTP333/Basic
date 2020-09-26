import time
import os
from Tools.mysql import MySql

class Commontool():

    def __init__(self,envi):
        self.mysql = MySql(envi)
        self.envi = envi
        self.dirname = os.path.join(os.getcwd(),"log")
        self.nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def getCustNo(self,cust_no=''):
        sqls = "select p_org_code from zs_org WHERE org_code = '%s'" % cust_no
        top_cust_no = self.mysql.searchs(sqls=sqls)[0][0]
        if top_cust_no == '0':
            top_cust_no = cust_no
        return top_cust_no

    def getTableNum(self,orderId=None,orderItemNo=''):
        #通过订单获取分表
        if orderId !=None:
            top_org_code = self.mysql.searchs("SELECT top_org_id from srcorder_info_index where gc_order_no='{}'".format(orderId))
        else:
            top_org_code = self.mysql.searchs("SELECT top_org_id from srcorder_info_index where gc_item_no='{}'".format(orderItemNo))

        top_org_code = top_org_code[0][0]
        table = self.mysql.searchs(
            "select table_num from gc_order_split_strategy_config where user_code='{}'".format(top_org_code))
        if table:
            table_num = list(table)[0][0]
        else:
            table_num = ''
        return table_num