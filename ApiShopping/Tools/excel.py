#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: opexcel.py
@time: 2019-06-15 15:50:50
@desc:
'''

import xlrd
from datetime import datetime
from xlrd import xldate_as_tuple

class ExcelFunc():

    def __init__(self):
        pass

    def readExcel(self,file, sheet_name, Level=''):
        workbook = xlrd.open_workbook(file)
        sheet = workbook.sheet_by_name(sheet_name)
        first_row_values = sheet.row_values(0)
        caseLevel = sheet.col_values(0)
        Row_values = []
        lineValues = 0
        for case in caseLevel:
            if Level =='':
                Row_values.append(lineValues)
            elif case == Level:
                Row_values.append(lineValues)
            lineValues = lineValues + 1
        num = 1
        caseList=[]
        caseName=[]

        for row_num in Row_values:
            row_values = sheet.row_values(row_num)
            caseName.append("【" + sheet_name + "-" + str(row_num) + "】" + "：" + row_values[2])

            if row_values:
                str_obj = []
            for i in range(len(first_row_values)):
                if i<=2:
                    continue
                ctype = sheet.cell(row_num, i).ctype  #ctype :  0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                cell = sheet.cell_value(row_num, i)
                if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
                    cell = int(cell)  # 浮点转成整型
                    cell = str(cell)  # 转成整型后再转成字符串，如果想要整型就去掉该行
                elif ctype == 3:
                    date = datetime(*xldate_as_tuple(cell, 0))
                    cell = date.strftime('%Y/%m/%d %H:%M:%S')
                elif ctype == 4:
                    cell = True if cell == 1 else False
                str_obj.append(cell)
            caseList.append(str_obj)
            num = num + 1
        return caseList,caseName

    def init_base(self,file='', sheet_name='维修方式查询接口', Level='L2'):
        caseData = self.readExcel(file=file, sheet_name=sheet_name, Level=Level)
        data = caseData[0]
        ids = [i for i in caseData[1]]
        return data, ids