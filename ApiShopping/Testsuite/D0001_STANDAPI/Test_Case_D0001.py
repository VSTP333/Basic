#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: Test_Case_D0001.py
@time: 2019-06-15 17:14:16
@desc:
'''
import sys,os
sys.path.append(os.path.abspath('%s/../..' % sys.path[0]))

from ApiShopping.API.D0001_STANDAPI.Base import StandApi
from Tools.tools import Common
import  pytest
import allure
from Tools.mysql import MySql
import json
from ToolsScript.T002_PushMessge import PushMessage
from ToolsScript.T003_PriceChange import PriceChange

class TestFunc_D0001:
    """标准API测试用例集"""

    def setup(self):
        """初始化环境"""
        envi = 'pre'
        appKey = '3cb2e898872a93782b60f31a4fa6696a'
        appSecret = '1787dafe14c385030d204ba2e2ade147'
        self.api = StandApi(envi=envi, appKey=appKey, appSecret=appSecret, isLog='Y')
        self.skus = '121347746'
        self.city = '025'
        self.mysql = MySql(envi=envi)
        self.common = Common(envi=envi)

    def teardown(self):
        pass

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_判断商品是否厂送接口')  # 接口名
    def test_judgeFacProduct_001(self):
        """政企商品API_判断商品是否厂送接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证商品是自营品"):  # 打印测试步骤
            skus = '121347740'
            # 预期结果
            expectedResults1 = '"results":[{"skuId":"%s","isFactorySend":"02"}],"errorList":[]'%skus
            # 实际结果
            actualResults1 = self.api.judgeFacProduct(skuIds=skus, cityId=self.city)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        with allure.MASTER_HELPER.step("验证商品是厂送品"):  # 打印测试步骤
            skus = '121347746'
            # 预期结果
            expectedResults2 = '"results":[{"skuId":"%s","isFactorySend":"01"}],"errorList":[]'%skus
            # 实际结果
            actualResults2 = self.api.judgeFacProduct(skuIds=skus, cityId=self.city)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言2 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_查询商品扩展信息接口(新)')  # 接口名
    def test_searchProdExtend_001(self):
        """政企商品API_查询商品扩展信息接口(新)"""  # 用例描述

        with allure.MASTER_HELPER.step("验证商品支持7天无理由"):  # 打印测试步骤
            # 预期结果
            expectedResults1 = '"skuId":"%s","returnGoods":"01","noReasonLimit":"7","noReasonTip":"7天无理由退货","increaseTicket":"01"'%self.skus
            # 实际结果
            actualResults1 = self.api.searchProdExtend(skuId=self.skus)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_获取商品簇信息接口')  # 接口名
    def test_getProductCluster_001(self):
        """政企商品API_获取商品簇信息接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取商品簇信息"):  # 打印测试步骤
            skus = '121347747'
            # 预期结果
            expectedResults1 = '{"clusterId":"2197","resultInfo":[{"skuId":"150027648","characterName":"尺码","characterValueId":"10001","characterValueName":"OO","imageShowFlag":"1"},{"skuId":"121347747","characterName":"尺码","characterValueId":"10002","characterValueName":"UU","imageShowFlag":"1"}]}'
            # 实际结果
            actualResults1 = self.api.getProductCluster(skuId=skus)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_政企商品类目搜索')  # 接口名
    def test_categorySearch_001(self):
        """政企商品API_政企商品类目搜索"""  # 用例描述

        with allure.MASTER_HELPER.step("验证政企商品类目搜索"):  # 打印测试步骤
            # 预期结果
            expectedResults1 = '"categoryId":"8b52260a-7383-493b-8dde-53b7b2706be6","categoryName":"文具","categoryLevel":"1","parentCategoryId":"0"'
            # 实际结果
            actualResults1 = self.api.categorySearch(keyword='空调')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_获取特殊商品池')  # 接口名
    def test_getSpecialGoods_001(self):
        """政企商品API_获取特殊商品池"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取特殊商品池"):  # 打印测试步骤
            # 预期结果
            expectedResults1 = '{"skuId":"761169091","cmmdtyType":"4"},{"skuId":"761169094","cmmdtyType":"3"},{"skuId":"520002051","cmmdtyType":"7"}'
            # 实际结果
            actualResults1 = self.api.getSpecialGoods(categoryId='d59ffaf1-83f7-495d-b3a1-668f219cc2d8')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_获取商品目录接口')  # 接口名
    def test_getCategory_001(self):
        """政企商品API_获取商品目录接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取商品目录接口"):  # 打印测试步骤
            # 预期结果
            expectedResults1 = '{"categoryId":"15257","categoryName":"单肩包"}'
            # 实际结果
            actualResults1 = self.api.getCategory()

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_获取商品池')  # 接口名
    def test_getPool_001(self):
        """政企商品API_获取商品池"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取商品池"):  # 打印测试步骤
            # 预期结果
            expectedResults1 = '{"skuId":"761109193","cmmdtyType":"1"},{"skuId":"150027648","cmmdtyType":"1"}'
            # 实际结果
            actualResults1 = self.api.getPool(categoryId='15257')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_获取商品详情接口')  # 接口名
    def test_getPictureDetail_001(self):
        """政企商品API_获取商品详情接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取商品详情接口正常返回"):  # 打印测试步骤
            # 预期结果
            expectedResults1 = '"getProdDetail":{"skuId":"%s","weight"'%self.skus
            # 实际结果
            actualResults1 = self.api.getPictureDetail(skuId=self.skus)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        with allure.MASTER_HELPER.step("验证获取商品详情接口返回包装清单字段"):  # 打印测试步骤
            skus = '750048822'
            # 预期结果
            expectedResults2 = '"packlisting":"烦烦烦撒阿萨德x1、11111x111、孟浩孟浩x2、快照增加x1、继续增加x1"'
            # 实际结果
            actualResults2 = self.api.getPictureDetail(skuId=skus)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_获取商品图片接口')  # 接口名
    def test_getPicture_001(self):
        """政企商品API_获取商品图片接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取商品图片接口"):  # 打印测试步骤
            # 预期结果
            expectedResults1 = '"resultInfo":[{"skuId":"%s","urls"'%self.skus
            # 实际结果
            actualResults1 = self.api.getPicture(skuId=self.skus)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_商品上下架状态查询接口')  # 接口名
    def test_batchStatus_001(self):
        """政企商品API_商品上下架状态查询接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证商品上下架状态查询接口"):  # 打印测试步骤
            # 预期结果
            expectedResults1 = '"onShelvesList":[{"skuId":"%s","state"'%self.skus
            # 实际结果
            actualResults1 = self.api.batchStatus(skuIds=self.skus)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_获取商品评价接口')  # 接口名
    def test_prodReview_001(self):
        """政企商品API_获取商品评价接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取商品评价接口"):  # 打印测试步骤
            # 预期结果
            expectedResults1 = '"resultInfo":[{"skuId":"%s","generalRate"'%self.skus
            # 实际结果
            actualResults1 = self.api.prodReview(skuIds=self.skus)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企商品API_获取套餐清单')  # 接口名
    def test_combinationProd_001(self):
        """政企商品API_获取套餐清单"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取套餐清单"):  # 打印测试步骤
            skus = '940001470'
            # 预期结果
            expectedResults1 = '"combinationProdDetails":[{"skuId":"121347584","num":"3"}'
            # 实际结果
            actualResults1 = self.api.combinationProd(skuId=skus)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企价格API_批量查询商品价格接口')  # 接口名
    def test_getPrice_001(self):
        """政企价格API_批量查询商品价格接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证批量查询商品价格接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = self.skus
            # 实际结果
            actualResults1 = self.api.getPrice(skuIds=self.skus,city=self.city)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企库存API_单个商品的精准库存查询接口')  # 接口名
    def test_getInventory_001(self):
        """政企库存API_单个商品的精准库存查询接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证单个商品的精准库存查询接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '"getInventory":{"resultInfo":[{"skuId":"%s","state"'%self.skus
            # 实际结果
            actualResults1 = self.api.getInventory(skuIds=self.skus,city=self.city,num=1)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企库存API_多商品的库存批量查询接口')  # 接口名
    def test_getStock_001(self):
        """政企库存API_多商品的库存批量查询接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证多商品的库存批量查询接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '"resultInfo":[{"skuId":"%s","state":0}'%self.skus
            # 实际结果
            actualResults1 = self.api.getStock(skuIds=self.skus,city=self.city)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_创建订单接口(新)')  # 接口名
    def test_addMixOrder_001(self):
        """政企订单API_创建订单接口(新)"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0',payType='08',nums='1',invoiceType=1,isInvoice=0,skuIds=self.skus,isservFee='N')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_批量查询订单行接口')  # 接口名
    def test_queryItemDetail_001(self):
        """政企订单API_批量查询订单行接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证批量查询订单行接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '"orderItemDtoList":[{"orderItemId":"10000181963101","orderId":"100001819631","orderStatus":"4"'
            # 实际结果
            actualResults1 = self.api.queryItemDetail(orderItem='10000181963101,10000181963301')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_售后进度查询接口')  # 接口名
    def test_queryServicescheDule_001(self):
        """政企订单API_获取自营换货售后进度"""  # 用例描述

        with allure.MASTER_HELPER.step("验证自营换货售后进度查询"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"orderId":"100001820470","orderItemIds":[{"orderItemId":"10000182047001","skuId":"121347740","afterSrvStatus":"9","pictureCode":"","afterSrvSchs":[{"afterSrvSch":"售后单处理完成","time":"20191120000020"},{"afterSrvSch":"售后单已完成取件","time":"20191119112110"},{"afterSrvSch":"退换货申请受理成功","time":"20191119111651"},{"afterSrvSch":"退换货申请提交成功","time":"20191119111539"}]}]}'
            # 实际结果
            actualResults1 = self.api.queryServicescheDule(orderId='100001820470',serviceType='2')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_售后进度查询接口')  # 接口名
    def test_queryServicescheDule_002(self):
        """政企订单API_获取自营退货售后进度"""  # 用例描述

        with allure.MASTER_HELPER.step("验证自营退货售后进度查询"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"orderId":"100001821886","orderItemIds":[{"orderItemId":"10000182188601","skuId":"121347740","afterSrvStatus":"15","pictureCode":"","afterSrvSchs":[{"afterSrvSch":"售后单处理完成","time":"20191129162233"},{"afterSrvSch":"退款处理中","time":"20191129162231"},{"afterSrvSch":"售后单已完成取件","time":"20191129162111"},{"afterSrvSch":"退换货申请受理成功","time":"20191129161322"},{"afterSrvSch":"退换货申请提交成功","time":"20191129160953"}]}]}'
            # 实际结果
            actualResults1 = self.api.queryServicescheDule(orderId='100001821886',serviceType='1')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_售后进度查询接口')  # 接口名
    def test_queryServicescheDule_003(self):
        """政企订单API_获取厂送换货售后进度"""  # 用例描述

        with allure.MASTER_HELPER.step("验证厂送换货售后进度查询"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"sn_responseContent":{"sn_body":{"queryServiceschedule":{"orderId":"100001821887","orderItemIds":[{"orderItemId":"10000182188701","skuId":"121347746","sheetId":"20191129501704000002","afterSrvStatus":"15","pictureCode":"","afterSrvSchs":[{"afterSrvSch":"您的换货单20191129501704000002已收货。","time":"20191129174736"},{"afterSrvSch":"您的换货单20191129501704000002已发货。","time":"20191129174412"},{"afterSrvSch":"供应商已确认为您换货，正在准备为您发货。","time":"20191129171049"},{"afterSrvSch":"供应商已收到您申请换货商品的寄退物流信息，请等待供货商鉴定结果。","time":"20191129171005"},{"afterSrvSch":"您申请换货的商品需要您寄送到如下地址：浙江杭州市滨江区滨江路31号,供货商联系电话：,联系人：赵四","time":"20191129170915"},{"afterSrvSch":"您的售后服务单20191129501704000002已提交供货商处理","time":"20191129170411"}],"returnInfo":[{"returnAddress":"浙江杭州市滨江区滨江路31号","returnPhone":"","returnName":"赵四"}]}]}}}}'
            # 实际结果
            actualResults1 = self.api.queryServicescheDule(orderId='100001821887',serviceType='2',orderItem='10000182188701',skuId='121347746',sheetId='20191129501704000002',online='Y')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_售后进度查询接口')  # 接口名
    def test_queryServicescheDule_004(self):
        """政企订单API_获取厂送退货售后进度"""  # 用例描述

        with allure.MASTER_HELPER.step("验证厂送退货售后进度查询"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"sn_responseContent":{"sn_body":{"queryServiceschedule":{"orderId":"100001821929","orderItemIds":[{"orderItemId":"10000182192901","skuId":"121347746","sheetId":"20191129501755000003","afterSrvStatus":"15","pictureCode":"","afterSrvSchs":[{"afterSrvSch":"退款完成，退款金额1.000000","time":"20191129175732"},{"afterSrvSch":"供货商同意退款","time":"20191129175725"},{"afterSrvSch":"供应商已收到您申请退货商品的寄退物流信息，请等待供货商鉴定结果。","time":"20191129175714"},{"afterSrvSch":"寄货申请已提交","time":"20191129175714"},{"afterSrvSch":"您申请退货的商品需要您寄送到如下地址：香港香港九龙区123，供货商联系电话：，联系人：李三","time":"20191129175618"},{"afterSrvSch":"您的售后服务单20191129501755000003已提交供货商处理","time":"20191129175537"}],"returnInfo":[{"returnAddress":"香港香港九龙区123","returnPhone":"","returnName":"李三"}]}]}}}}'
            # 实际结果
            actualResults1 = self.api.queryServicescheDule(orderId='100001821929',serviceType='1',orderItem='10000182192901',skuId='121347746',sheetId='20191129501755000003',online='Y')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_支付宝支付接口')  # 接口名
    def test_aliPay_001(self):
        """政企订单API_支付宝支付接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-支付宝支付方式"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0',payType='05',nums='1',invoiceType=1,isInvoice=0,skuIds=self.skus,isservFee='N')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  #政企订单号

        with allure.MASTER_HELPER.step("验证支付宝支付接口"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"sn_responseContent":{"sn_body":{"createAlipay":{"service":"create_direct_pay_by_user"'
            # 实际结果
            actualResults2 = self.api.aliPay(orderId=orderId, channelType='PC')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_PO单信息提交')  # 接口名
    def test_poOrderId_001(self):
        """政企订单API_PO单信息提交"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下预占单-账期支付方式"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='1',payType='08',nums='1',invoiceType=1,isInvoice=0,skuIds=self.skus,isservFee='N')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  #政企订单号

        with allure.MASTER_HELPER.step("验证PO单信息提交"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"sn_responseContent":{"sn_body":{"addPoorderid":{"success":"Y"}}}}'
            # 实际结果
            actualResults2 = self.api.poOrderId(orderId=orderId,porderId='100001819636-1',orderItemId=str(orderId)+'01',skuId=self.skus,num='1',porderItemId='201909021559-1',remark='po单提交')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_订单行对账接口')  # 接口名
    def test_queryOrderItem_001(self):
        """政企订单API_订单行对账接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证订单行对账接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"sn_responseContent":{"sn_body":{"queryOrderitem":{"sumPrice":"22.00","orderItemInfoList":[{"orderItemId":"10000181968301","skuNum":"1","orderItemPrice":"6.00","orderItemStatus":"1"},{"orderItemId":"10000181967701","skuNum":"1","orderItemPrice":"6.00","orderItemStatus":"1"},{"orderItemId":"10000181966601","skuNum":"1","orderItemPrice":"6.00","orderItemStatus":"1"},{"orderItemId":"10000181963601","skuNum":"2","orderItemPrice":"2.00","orderItemStatus":"1"},{"orderItemId":"10000181955201","skuNum":"2","orderItemPrice":"2.00","orderItemStatus":"1"}],"orderSum":"5","pageNum":"1","totalPage":"1"}}}}'
            # 实际结果
            actualResults1 = self.api.queryOrderItem(startDate="2019-11-14",endDate="2019-11-15",orderItemStatus="1",companyCusNo='')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)


    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_企业汇款支付')  # 接口名
    def test_bankTransfer_001(self):
        """政企订单API_企业汇款支付"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-企业汇款支付方式"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0',payType='12',nums='1',invoiceType=1,isInvoice=0,skuIds=self.skus,isservFee='N',companyCustNo='19911010084@163.com')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  #政企订单号

        with allure.MASTER_HELPER.step("验证PO单信息提交"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"sn_responseContent":{"sn_body":{"createBanktransfer":{"accountCode":"'
            # 实际结果
            actualResults2 = self.api.bankTransfer(phoneNum='15811084772',orderId=orderId)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_取消预占库存订单接口')  # 接口名
    def test_cancleOrder_001(self):
        """政企订单API_取消预占库存订单接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-账期预占库存"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='1',payType='08',nums='1',invoiceType=1,isInvoice=0,skuIds=self.skus,isservFee='N',companyCustNo='19911010084@163.com')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  #政企订单号

        with allure.MASTER_HELPER.step("验证取消预占库存"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"sn_responseContent":{"sn_body":{"deleteRejectOrder":{"unCampSuccess":"Y"}}}}'
            # 实际结果
            actualResults2 = self.api.cancleOrder(orderId=orderId)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_查询单个订单详细')  # 接口名
    def test_orderDetail_001(self):
        """政企订单API_查询单个订单详细"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-账期支付"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0',payType='08',nums='1',invoiceType=1,isInvoice=0,skuIds=self.skus,isservFee='N',companyCustNo='')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  #政企订单号

        with allure.MASTER_HELPER.step("验证查询单个订单详细"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"sn_responseContent":{"sn_body":{"getOrderDetail":{"orderId":"%s","companyName":"北京平谷大桃一有限公司"'%orderId
            # 实际结果
            actualResults2 = self.api.orderDetail(orderId=orderId)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企订单API_获取订单状态接口')  # 接口名
    def test_getStatus_001(self):
        """政企订单API_获取订单状态接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-账期支付"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0',payType='08',nums='1',invoiceType=1,isInvoice=0,skuIds=self.skus,isservFee='N',companyCustNo='')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  #政企订单号

        with allure.MASTER_HELPER.step("验证获取订单状态接口"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"sn_responseContent":{"sn_body":{"getOrderStatus":{"orderId":"%s","orderStatus":"3"'%orderId
            # 实际结果
            actualResults2 = self.api.getStatus(orderId=orderId)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言2 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企物流API_获取订单物流详情（新）')  # 接口名
    def test_getOrderLogistNew_001(self):
        """政企物流API_获取订单物流详情（新）"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取订单物流详情（新）"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"operateState":"已分配送货人员【数据仓库专用二12512342333】，等待收货","operateTime":"20191220123700"},{"operateState":"送货服务已取消，因商品存在破损/质量问题，您已选择拒收，欢迎您再次光临","operateTime":"20191220123705"}],"orderItemIds":[{"orderItemId":"10000183602501","skuId":"121347740"'
            # 实际结果
            actualResults1 = self.api.getOrderLogistNew(orderId='100001836025',orderItemId='10000183602501',skuId='121347740')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企物流API_获取订单包裹信息接口')  # 接口名
    def test_getOrderLogistNew_001(self):
        """政企物流API_获取订单包裹信息接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取订单包裹信息接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '"packageList":[{"skuList":[{"orderItemId":"10000182577801","skuId":"121347746","skuNum":"2"}],"packageCode":"3828743898704"}],"expressCompany":"韵达快运","logisticNumber":"3828743898704","receiveTime":"2019-12-11 14:21:01","shippingTime":"2019-12-11 14:18:21"}'
            # 实际结果
            actualResults1 = self.api.getLogistDetail(orderId='100001825778',orderItemId='10000182577801')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企物流API_获取订单物流详情')  # 接口名
    def test_getOrderLogist_001(self):
        """政企物流API_获取订单物流详情"""  # 用例描述

        with allure.MASTER_HELPER.step("验证获取订单物流详情"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"operateState":"已分配送货人员【数据仓库专用二12512342333】，等待收货","operateTime":"20191220123700"},{"operateState":"送货服务已取消，因商品存在破损/质量问题，您已选择拒收，欢迎您再次光临","operateTime":"20191220123705"}'
            # 实际结果
            actualResults1 = self.api.getOrderLogist(orderId='100001836025',orderItemId='10000183602501',skuId='121347740')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企物流API_物流时效接口')  # 接口名
    def test_getShipTime_001(self):
        """政企物流API_物流时效接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证物流时效接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"skuId":"121347740","isDelivery":"Y","deliveryToVillageFlag":"1","supplierTel":"","installType":"2","srvCmmdtyCode":"FW99"'
            # 实际结果
            actualResults1 = self.api.getShipTime(skuId=self.skus,addrDetail="南京")

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企物流API_物流运费接口')  # 接口名
    def test_getShipCarriage_001(self):
        """政企物流API_物流运费接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证物流运费接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"sn_responseContent":{"sn_body":{"getShipCarriage":{"freightFare":0.0}}}}'
            # 实际结果
            actualResults1 = self.api.getShipCarriage(skuId=self.skus,piece="1",cityId="025",districtId="11",townId="",addrDetail="国宸餐饮")

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企物流API_厂送商品确认收货接口')  # 接口名
    def test_conFacProduct_001(self):
        """政企物流API_厂送商品确认收货接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-厂送品账期支付"):  # 打印测试步骤

            sku = '121347746'
            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0',payType='08',nums='1',invoiceType=1,isInvoice=0,skuIds=sku,isservFee='N',companyCustNo='')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  #政企订单号

        with allure.MASTER_HELPER.step("验证厂送商品确认收货"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"sn_responseContent":{"sn_body":{"confirmFacProduct":{"apiIsSuccess":"Y"}}}}'
            # 实际结果
            actualResults2 = self.api.conFacProduct(orderId=orderId, skuId=sku)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言2 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)


    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企发票API_政企订单补开发票')  # 接口名
    def test_confirmInvoice_001(self):
        """政企发票API_政企订单补开发票"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-账期支付暂不开票"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0',payType='08',nums='1',invoiceType=1,isInvoice=0,skuIds=self.skus,isservFee='N',companyCustNo='')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  #政企订单号

        self.common.updatOrderStatus(orderId=orderId,types='access')   #修改订单状态为妥投

        with allure.MASTER_HELPER.step("验证政企订单补开增票"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '"b2cItemNo":"%s"'%(orderId+'01')
            # 实际结果
            actualResults2 = self.api.confirmInvoice(gcOrderNo=orderId,invoiceType=6,invoiceContent=22,markId=orderId)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言2 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企发票API_发票信息查询')  # 接口名
    def test_getInvoice_001(self):
        """政企发票API_发票信息查询"""  # 用例描述

        with allure.MASTER_HELPER.step("验证发票信息查询"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"invoiceState":"2","invoiceid":"01350782","invoiceCode":"72520135","invoiceDate":"2019-12-19"'
            # 实际结果
            actualResults1 = self.api.getInvoice(field='100001835228',type='1')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企发票API_电子发票查询接口')  # 接口名
    def test_eleInvoice_001(self):
        """政企发票API_电子发票查询接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证电子发票查询接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"sn_responseContent":{"sn_body":{"getEleinvoice":{"orderId":"100001835298","eleInvoices":[{"orderItemId":"10000183529801","skuId":"000000000121347740","invoiceBlueUrl":"http://sdosspre1.cnsuning.com/esps/invoice_pdf/15754311876431187644e689f090-49ff-4a0d-a55e-098dbe0b4d60.pdf"}]}}}}'
            # 实际结果
            actualResults1 = self.api.eleInvoice(orderId='100001835298',orderItemId='10000183529801',skuId='121347740')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企售后API_退货申请接口（新）')  # 接口名
    def test_returnPartOrder_001(self):
        """政企售后API_退货申请接口（新）"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-账期支付"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0', payType='08', nums='1', invoiceType=1, isInvoice=0,
                                                  skuIds=self.skus, isservFee='N', companyCustNo='')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

            # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  # 政企订单号

        self.common.updatOrderStatus(orderId=orderId, types='access')  # 修改订单状态为妥投

        with allure.MASTER_HELPER.step("验证退货申请接口"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"orderId":"%s","infoList":[{"skuId":"%s","status":"1"' % (orderId,self.skus)
            # 实际结果
            actualResults2 = self.api.returnPartOrder(skuId=self.skus,num='1',orderId=orderId,reason='0301',reasonDetails='ceshi',bankName='03',cardUsername='王大力',cardNumber='6200121394857114')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言2 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企其他API_在线支付接口')  # 接口名
    def test_createOnlinePay_001(self):
        """政企其他API_在线支付接口-易付宝"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-易付宝支付"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0', payType='01', nums='1', invoiceType=1, isInvoice=0,
                                                  skuIds=self.skus, isservFee='N', companyCustNo='')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

            # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  # 政企订单号

        with allure.MASTER_HELPER.step("验证在线支付接口-易付宝支付"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"createOnlinepay":{"payUrl":"https://zspre.cnsuning.com/payOnlineApi/initPcPayInfo.htm"'
            # 实际结果
            actualResults2 = self.api.createOnlinePay(orderId=orderId,payway='01')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言2 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企其他API_在线支付接口')  # 接口名
    def test_createOnlinePay_002(self):
        """政企其他API_在线支付接口-网银"""  # 用例描述

        with allure.MASTER_HELPER.step("验证创建订单接口(新)下单-网银支付"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = 'addMixpayorder":{"orderId":'
            # 实际结果
            actualResults1 = self.api.addMixOrder(orderType='0', payType='020', nums='1', invoiceType=1, isInvoice=0,
                                                  skuIds=self.skus, isservFee='N', companyCustNo='')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

            # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        actualResults1 = json.loads(actualResults1)
        orderId = actualResults1["sn_responseContent"]["sn_body"]["addMixpayorder"]["orderId"]  # 政企订单号

        with allure.MASTER_HELPER.step("验证在线支付接口-网银支付"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"createOnlinepay":{"payUrl":"https://zspre.cnsuning.com/payOnlineApi/initPcPayInfo.htm"'
            # 实际结果
            actualResults2 = self.api.createOnlinePay(orderId=orderId,payway='020')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言2 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企其他API_是否支持货到付款接口')  # 接口名
    def test_getPaymentWay_001(self):
        """政企其他API_是否支持货到付款接口"""  # 用例描述

        with allure.MASTER_HELPER.step("验证是否支持货到付款接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"sn_responseContent":{"sn_body":{"getPaymentway":{"codPos":"N","codCash":"N"}}}}'
            # 实际结果
            actualResults1 = self.api.getPaymentWay(skuId='121347590')

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企其他API_价格变动消息查询接口')  # 接口名
    def test_getPriceMessage_001(self):
        """政企其他API_价格变动消息查询接口"""  # 用例描述

        PriceChange(cmmdtyCode=self.skus,cityCode="000001000173")

        with allure.MASTER_HELPER.step("验证价格变动消息查询接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"result":[{"cmmdtyCode":"%s"'%self.skus
            # 实际结果
            actualResults1 = self.api.getPriceMessage()

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企其他API_查询预存款金额接口')  # 接口名
    def test_preDepositBalance_001(self):
        """政企其他API_查询预存款金额接口"""  # 用例描述

        envi = 'pre'
        appKey = 'c278df52d4fb2fc4ad20b98ed523c189'
        appSecret = 'cc95a5cce45fbe52995fe7398e7888bc'
        api = StandApi(envi=envi, appKey=appKey, appSecret=appSecret, isLog='Y')

        with allure.MASTER_HELPER.step("验证查询预存款金额接口"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '{"getPreDepositBalance":{"preDepositBalance"'
            # 实际结果
            actualResults1 = api.preDepositBalance()

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企其他API_查询消息')  # 接口名
    def test_getMessage_001(self):
        """政企其他API_查询消息"""  # 用例描述

        PushMessage().Bill(account='19911010083@163.com', custNo='7017966447')

        with allure.MASTER_HELPER.step("验证查询消息-账单消息"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '"pin":"19911010083@163.com"'
            # 实际结果
            actualResults1 = self.api.getMessage(type=17)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

    @pytest.mark.case_L0  # 用例等级
    @allure.MASTER_HELPER.feature('标准API主流程回归校验')  # 用例分类
    @allure.MASTER_HELPER.story('政企其他API_删除消息')  # 接口名
    def test_deleteMessage_001(self):
        """政企其他API_删除消息"""  # 用例描述

        with allure.MASTER_HELPER.step("验证查询消息-账单消息"):  # 打印测试步骤

            # 预期结果
            expectedResults1 = '"pin":"19911010083@163.com"'
            # 实际结果
            actualResults1 = self.api.getMessage(type=17)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults1))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults1))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults1 in str(actualResults1)

        msg_id = json.loads(actualResults1)["sn_responseContent"]["sn_body"]["getMessage"]["resultInfo"]
        for i in msg_id:
            id = i["id"]

        with allure.MASTER_HELPER.step("验证删除消息-账单消息"):  # 打印测试步骤

            # 预期结果
            expectedResults2 = '{"sn_responseContent":{"sn_body":{"deleteMessage":{"isDelSuccess":"Y"}}}}'
            # 实际结果
            actualResults2 = self.api.deleteMessage(id=id)

            allure.MASTER_HELPER.attach('预期结果：', "{}".format(expectedResults2))
            allure.MASTER_HELPER.attach('实际结果：', "{}".format(actualResults2))

        # 断言1 ：实际结果包含预期结果
        assert expectedResults2 in str(actualResults2)

if __name__ == '__main__':
    pytest.main(['-m=case_L0', '-q', '-n=3', '--alluredir', 'report'])
    # pytest.main(['-m=case_L0','-q','--tb=short','-n=3','--alluredir', 'report'])
    os.system("allure generate report -o report/html")