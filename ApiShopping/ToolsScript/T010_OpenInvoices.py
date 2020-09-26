#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: T010_OpenInvoices.py
@time: 2019-11-25 11:10:12
@desc:暂作为联通系开票使用
'''

from Tools.tools import Common
import time
from Tools.operatetool import Commontool
api=Common(envi='pre')
common = Commontool(envi='pre')

def insertInvoice(itemNo=''):
    now_times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    amount_sum = api.getInvoicePice(itemNo,isRe='Y')
    invoice_id = str(int(time.time() * 1000000))[4:12]
    invoice_code = str(int(time.time() * 1000000))[-8:]
    invoice_date = time.strftime('%Y-%m-%d 00:00:00', time.localtime())
    gc_item_no = itemNo.split(",")
    pdfUrl = 'http://sdosspre1.cnsuning.com/esps/invoice_pdf/15754311876431187644e689f090-49ff-4a0d-a55e-098dbe0b4d60.pdf'

    # 获取分表号
    for i in range(len(gc_item_no)):

        table = common.getTableNum(orderItemNo=gc_item_no[i])
        item_resu = api.mysql.searchs("select cust_no,oms_item_no,unit_price,quantiy,promot_tax from srcorder_item%s where  gc_item_no = '%s'" %(table,gc_item_no[i]))
        cust_no = item_resu[0][0]         #下单会员编号
        oms_item_no = item_resu[0][1]     #oms订单行号
        unit_price = item_resu[0][2]      #商品单价
        quantiy = item_resu[0][3]         #商品数量
        promot_tax = item_resu[0][4]      #商品数量
        qu_sum = round(unit_price*quantiy,2)       #订单行总价

        inv_taxamount = round(amount_sum * float(promot_tax),2)  #税额
        naked_amount = round(amount_sum - inv_taxamount,2)   #不含税价
        top_cust_no = common.getCustNo(cust_no)
        tab_num = int(top_cust_no)%64

        sql = "update invoice_merge_reissue_order_send_status{} set invoice_id='{}' ,invoice_code='{}',invoice_date='{}',\
        amount_sum='{}',mail_code='Y02',mail_number='3828743898704',mail_type='韵达快运',mail_time='{}',pdfUrl='{}',naked_price='{}',tax_amount='{}',send_state='2',invoice_status='0' where gc_item_no='{}' and znxbj='0'".format(str(tab_num), \
                                                                                                                                                                                                            invoice_id,invoice_code,invoice_date,amount_sum,invoice_date,pdfUrl,naked_amount,inv_taxamount,gc_item_no[i])
        api.mysql.updates(sql)

        header_resu = api.mysql.searchs("select invoice_title from srcorder_header{} where gc_order_no='{}'".format(table,gc_item_no[i][0:-2]))
        inv_title = header_resu[0][0]


        reissue_resu = api.mysql.searchs("select tax_no,commdty_code,commdty_name,tax_rate,bill_number,invoice_type,sn_mark_id from invoice_merge_reissue_order_info{} where gc_item_no='{}'".format(str(tab_num),gc_item_no[i]))
        cert_no = reissue_resu[0][0]
        cmmdty_code = reissue_resu[0][1]
        cmmdty_name = reissue_resu[0][2]
        tax_rate = reissue_resu[0][3]
        bill_number = reissue_resu[0][4]
        invoice_type = reissue_resu[0][5]  #发票类型
        sn_mark_id = reissue_resu[0][6] # 补开批次号
        # print(sn_mark_id)

        times = time.strftime('%Y%m%d%H%M%S', time.localtime())
        fpqqlsh = str(times)+cust_no+'&'+oms_item_no

        if invoice_type==5 or invoice_type==1:  #增票
            inv_type = '01'
        elif invoice_type==9:   #电子票
            inv_type = '04'
        elif invoice_type==8:   #普票
            inv_type = '06'

        # isTrue = api.mysql.searchs("SELECT 1 FROM invoice_merge_reissue_invoice_info%s WHERE gc_item_no = '%s'" % (tab_num,gc_item_no[i]))
        # if not isTrue[0][0] :
            # api.mysql.deletes("DELECT FROM invoice_merge_reissue_invoice_info%s where gc_item_no = '%s'" % (table,gc_item_no[i]))

        sql1 = "INSERT INTO invoice_merge_reissue_invoice_info%s  \
               (`top_cust_no`, `gc_order_no`, `gc_item_no`, `order_item_id`,`fpqqlsh`,`biz_type`,`sale_org`, `sale_org_name`,  \
               `sale_org_no`,`inv_type`,`znxbj`, `inv_status`,`inv_code`, `inv_no`, `inv_date`, `inv_amount`, `naked_amount`, `inv_taxamount`,`pdf_url`,`inv_title`,`cert_no`,`cmmdty_code`,`cmmdty_name`,`price`, `number`, `amount`,`transport_fee`,`discount_sum`, `tax_rate`,`tax_code`, `create_time`, `update_time`, `b2c_order_id`, `bill_number`, `batch_no`,mail_code, mail_type, mail_number, mail_time) VALUES  \
               ('%s','%s','%s','%s','%s','ZQHB','5016','南京苏宁易购电子商务有限公司','140301203909248475','%s','1','0','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','0','0','%s','1090416020000000000','%s','%s','%s','%s','1','Y02','韵达快运','3828743898704','%s')" % \
               (str(tab_num),top_cust_no,gc_item_no[i][0:-2],gc_item_no[i],oms_item_no,fpqqlsh,inv_type,invoice_id,invoice_code,now_times,amount_sum,naked_amount,inv_taxamount,pdfUrl,inv_title,cert_no,cmmdty_code,cmmdty_name,unit_price,quantiy,str(qu_sum),tax_rate,now_times,now_times,gc_item_no[i][0:-2],bill_number,invoice_date)

        api.mysql.inserts(sql1)
        isTrue =  api.mysql.searchs("SELECT 1 FROM invoice_base_info WHERE batch_no = '%s'" % sn_mark_id)
        if isTrue :
            pass
        else:
            sql2 = "INSERT INTO invoice_base_info (invoice_sn, batch_no, invoice_id, invoice_code, invoice_status," \
                   " invoice_date, naked_price, tax_rate, tax_amount, invoice_amount, invoice_type, send_method, send_no," \
                   " send_date, send_state, create_time, update_time, app_key, cell_no, supplementary_status," \
                   " supplementary_time, pdfUrl, new_flag, new_status, send_company_code, verification_code, inv_status) " \
                   "VALUES ('%s', '%s', '%s', '%s', '1', '%s', '%s', '%s', '%s', '%s', '%s', '韵达快运', '3828743898704', " \
                   "'%s', '%s', '%s', '%s', NULL, '0', '0', NULL, '', '0', '5', 'Y02', NULL, '0');"% \
                   (bill_number,sn_mark_id,invoice_id,invoice_code,now_times,naked_amount,tax_rate,inv_taxamount,amount_sum,invoice_type,
                    now_times,'3',invoice_date,invoice_date)
            api.mysql.inserts(sqls=sql2)
        mark_id = sn_mark_id.split('-')[0]
        sql3 = "INSERT INTO invoice_common_info (batch_no, mark_id, recive_name, recive_phone, recive_province," \
               " recive_city, recive_district, recive_town, recive_address, full_address, cust_no, invoice_org, invoice_type," \
               " invoice_content, invoice_title, invoice_date, naked_price, tax_amount, invoice_amount, create_time," \
               " update_time, company_name, license_no, tax_no, reg_add, reg_tel, reg_bank, reg_account, app_key," \
               " payorg_name, push_status, remark) VALUES ('%s', '%s', '余毫', '18566296202', NULL, NULL, NULL, NULL, " \
               "'华丽的爱看的反思', NULL, '7018166120', '5016', '1', '明细', '太平金融', '%s', '%s', '%s', '%s', '%s', NULL," \
               " '太平金融', NULL, '123456789054321', '北京海淀区', '010-87654321', '中国银行', '1111111111111', NULL, " \
               "NULL, NULL, '结算单号:FS2020062411524865');" % (sn_mark_id,mark_id,now_times,naked_amount,inv_taxamount,amount_sum,invoice_date)

        api.mysql.inserts(sqls=sql3)
        isTrue = api.mysql.searchs("SELECT 1 from invoice_order_relation WHERE  b2c_item_no = '%s'" % gc_item_no[i])
        orderitemNo = api.mysql.searchs("SELECT order_item_no from srcorder_info_index WHERE gc_item_no = '%s'" % gc_item_no[i])
        orderitemNo = orderitemNo[0][0]
        if isTrue:
            api.mysql.updates("UPDATE invoice_order_relation SET  invoice_sn='%s', batch_no='%s',"
                              " order_item_no='%s', invoice_status='3', is_send='0', update_time='%s', "
                              "order_time='%s', tax_rate='%s' WHERE b2c_item_no='%s';" % (bill_number,sn_mark_id,orderitemNo,invoice_date,invoice_date,tax_rate,gc_item_no[i]))
        else:
            sql4 = "INSERT INTO gcmspre1.invoice_order_relation (invoice_sn, batch_no, b2c_item_no, commdty_quanity, " \
                   "order_item_no, invoice_status, is_send, update_time, order_time, tax_rate) VALUES " \
                   "('%s', '%s', '%s', '1', '%s', '3', '0', '%s', '%s', '%s');" % (bill_number,sn_mark_id,itemNo,orderitemNo,invoice_date,invoice_date,tax_rate)
            a = api.mysql.inserts(sqls=sql4)
            print(a)

if __name__ == '__main__':

    itemNo = '10000207342801'

    insertInvoice(itemNo=itemNo)