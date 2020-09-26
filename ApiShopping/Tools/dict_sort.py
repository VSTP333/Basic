#!/usr/bin/env python
# encoding: utf-8
'''
@author: 18056678（郭海龙）
@project: ApiShopping
@file: dict_sort.py
@time: 2020-01-21 09:20:34
@desc:字典排序，按value排序时，不支持str
'''
from Tools.md5 import Md5
class Dict_Sort(object):
    def dict_sort_by_key(self,di=None):
        dict_sorted = sorted(di.items(), key=lambda asd:asd[0],reverse = False)
        new_dict = dict(dict_sorted)
        return new_dict
    def dict_sort_by_value(self,di=None):
        dict_sorted = sorted(di.items(), key=lambda asd: asd[1], reverse=False)
        new_dict = dict(dict_sorted)
        return new_dict

if __name__ == '__main__':
    data = ''
    di = {"sku_list":[{"sku_Id":"yqb4120313","out_sku_id":"121347740","count":2}],"country":"中国","province":"江苏省","city":"南京市","county":"鼓楼区"}
    DS = Dict_Sort()
    nd = DS.dict_sort_by_key(di=di)
    # print(nd)
    for key,value in nd.items():
        data = data + key + str(value).strip()
    new_data = data.replace("\'","\"").replace(" ","")
    sign = '09055208-2aed-4618-8e9e-ab51bdca203d' + new_data + '09055208-2aed-4618-8e9e-ab51bdca203d'
    # print(sign)
    sign_md5 = Md5().getMd5_32(text=sign,upper=True)
    print(sign_md5)
