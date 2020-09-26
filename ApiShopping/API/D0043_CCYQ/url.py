#!/usr/bin/env python
# encoding: utf-8
'''
@author: 18056678（郭海龙）
@project: ApiShopping
@file: url.py
@time: 2019-12-24 17:44:13
@desc:
'''
class Link():
    class GetLogisticsDetail():
        url = '/inserv/ccyq/logist/getLogistdetail'

    class GetShelvesStatus():
        url = '/inserv/ccyq/product/getShelves'

    class CheckStockStatus():
        url = '/inserv/ccyq/product/getStocks'

    class GetPriceAndTaxcode():
        url = '/inserv/ccyq/product/queryPriceAndTax'

    class CheckSaleStatus():
        url = '/inserv/ccyq/product/saleStatus'

    class HandMsg():
        url = '/inserv/ccyq/handleMsg'
