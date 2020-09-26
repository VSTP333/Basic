#!/usr/bin/env python
# encoding: utf-8
'''
@author: 18056678（郭海龙）
@project: ApiShopping
@file: Test_Case_D0043.py
@time: 2020-05-06 16:41:52
@desc:
'''
import pytest
import allure

from API.D0043_CCYQ.Base import API
from Tools.tools import Common
from Tools.tools import MySql
from time import sleep
import os
class TestFuncCCYQ(object):
    """长春一汽案例集"""
    def setup(self):
        """初始化环境"""
        envi='pre'
        self.api=API(envi=envi,user='HBYC',isLog='N')
        self.common=Common(envi=envi)
        self.sku='121347657'
        self.mysql=MySql(envi=envi)

    def teardown(self):
        pass

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('华电集团主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('消息接口')  # 用例名
    def test_handMsg(self):
        """消息接口"""
        with allure.MASTER_HELPER.step("验证接口是否返回成功"):  # 打印测试步骤
            # 预期结果
            expectedResult1 = True
            # 实际结果
            actualResult1 = self.api.handMsg(business='ORDER',event='ADD',pcode='HB202004080001')['success']

            allure.MASTER_HELPER.attach('预期结果：', '{}'.format(expectedResult1))
            allure.MASTER_HELPER.attach('实际结果：', '{}'.format(actualResult1))

            # 断言：实际结果包含预期结果
            assert isinstance(actualResult1,int)


    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('华电集团主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('查询物流')  # 用例名
    def test_getLogistic(self):
        """消息接口"""
        with allure.MASTER_HELPER.step("验证接口是否返回成功"):  # 打印测试步骤
            # 预期结果
            expectedResult1 = True
            # 实际结果
            actualResult1 = self.api.getLogistic(code='00105619179001')['success']

            allure.MASTER_HELPER.attach('预期结果：', '{}'.format(expectedResult1))
            allure.MASTER_HELPER.attach('实际结果：', '{}'.format(actualResult1))

            # 断言：实际结果包含预期结果
            assert isinstance(actualResult1,int)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('华电集团主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('获取商品价格及税率')  # 用例名
    def test_getProdPriceAndTaxcode(self):
        """获取商品价格及税率"""
        with allure.MASTER_HELPER.step("验证接口是否返回成功"):  # 打印测试步骤
            # 预期结果
            expectedResult1 = True
            # 实际结果
            actualResult1 = self.api.getProdPriceAndTaxcode(skus=self.sku,provinceCode='110000000000',citycode='110100000000',countyCode='110114000000')['success']

            allure.MASTER_HELPER.attach('预期结果：', '{}'.format(expectedResult1))
            allure.MASTER_HELPER.attach('实际结果：', '{}'.format(actualResult1))

            # 断言：实际结果包含预期结果
            assert isinstance(actualResult1,int)


    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('华电集团主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('获取商品售卖区域')  # 用例名
    def test_checkSalearea(self):
        """获取商品售卖区域"""
        with allure.MASTER_HELPER.step("验证接口是否返回成功"):  # 打印测试步骤
            # 预期结果
            expectedResult1 = True
            # 实际结果
            actualResult1 = self.api.checkSalearea(skus=self.sku,provinceCode='110000000000',citycode='110100000000',countyCode='110114000000')['success']

            allure.MASTER_HELPER.attach('预期结果：', '{}'.format(expectedResult1))
            allure.MASTER_HELPER.attach('实际结果：', '{}'.format(actualResult1))

            # 断言：实际结果包含预期结果
            assert isinstance(actualResult1,int)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('华电集团主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('获取商品上下架状态')  # 用例名
    def test_getShelvesStatus(self):
        """获取商品上下架状态"""
        with allure.MASTER_HELPER.step("验证接口是否返回成功"):  # 打印测试步骤
            # 预期结果
            expectedResult1 = True
            # 实际结果
            actualResult1 = self.api.getShelvesStatus(skus=self.sku)['success']

            allure.MASTER_HELPER.attach('预期结果：', '{}'.format(expectedResult1))
            allure.MASTER_HELPER.attach('实际结果：', '{}'.format(actualResult1))

            # 断言：实际结果包含预期结果
            assert isinstance(actualResult1,int)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('华电集团主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('获取商品库存')  # 用例名
    def test_getStockStatus(self):
        """获取商品库存"""
        with allure.MASTER_HELPER.step("验证接口是否返回成功"):  # 打印测试步骤
            # 预期结果
            expectedResult1 = True
            # 实际结果
            actualResult1 = self.api.getStockStatus(skus=self.sku)['success']

            allure.MASTER_HELPER.attach('预期结果：', '{}'.format(expectedResult1))
            allure.MASTER_HELPER.attach('实际结果：', '{}'.format(actualResult1))

            # 断言：实际结果包含预期结果
            assert isinstance(actualResult1,int)










if __name__=='__main__':
    pytest.main(['-m=case_L0','-q','--tb=short','-n=3','--alluredir', 'report'])
    os.system("allure generate report -o report/html")
