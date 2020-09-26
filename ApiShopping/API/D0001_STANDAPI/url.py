#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: url.py
@time: 2019-05-09 11:44:57
@desc:标准api接口报文
'''

class StandConfig():
    datas = {
        "appKey": None,
        "format": "json",
        "appMethod": None,
        "reqParam": None,
        "sdkType": "JAVA",
        "appRequestTime": None,
        "signInfo": None
    }

    class GetPrice():
        method = "suning.govbus.price.query"
        data = '<sn_request><sn_body><queryPrice><cityId>%(city)s</cityId>%(skus)s</queryPrice></sn_body></sn_request>'

    class GetInventory():
        method = "suning.govbus.inventory.get"
        data = "<sn_request><sn_body><getInventory>%(skuIds)s\
        <cityId>%(city)s</cityId><countyId>%(countyId)s</countyId></getInventory></sn_body></sn_request>"

    class GetStock():
        method = "suning.govbus.mprodstock.query"
        data = "<sn_request><sn_body><queryMpStock>%(skus)s<cityId>%(cityId)s</cityId></queryMpStock></sn_body></sn_request>"

    class AddOrder():
        method = "suning.govbus.order.add"
        data = "<sn_request><sn_body><addOrder>\
        <provinceId>%(province)s</provinceId>\
        <zip>210000</zip>\
        <payment>%(payTpye)s</payment>\
        <orderType>%(orderType)s</orderType>\
        <invoiceState>%(invoiceState)s</invoiceState>\
        <invoiceType>%(invoiceType)s</invoiceType>\
        <tradeNo>%(tradeNo)s</tradeNo>\
        <cityId>%(city)s</cityId>\
        <remark>跑跑跑标准3.0</remark>\
        <townId>%(townId)s</townId>\
        <companyCustNo>%(companyCustNo)s</companyCustNo>\
        %(skuInfo)s\
        <invoiceTitle>老订单接口</invoiceTitle>\
        <taxNo>123456789012345</taxNo>\
        <servFee>%(servFee)s</servFee>\
        <amount>%(amount)s</amount>\
        <address>%(address)s</address>\
        <email>yanhua1634@163.com</email>\
        <receiverName>段启阳</receiverName>\
        <telephone>010-67083399</telephone>\
        <countyId>%(county)s</countyId>\
        <mobile>15811084770</mobile>\
        <invoiceContent>1</invoiceContent>\
        </addOrder></sn_body></sn_request>"

    class AddMixOrder():
        method = "suning.govbus.mixpayorder.add"
        data = "<sn_request><sn_body><addMixpayorder>\
        <payment>%(payTpye)s</payment>\
        <orderType>%(orderType)s</orderType>\
        <provinceId>%(province)s</provinceId>\
        <cityId>%(city)s</cityId>\
        <countyId>%(county)s</countyId>\
        <invoiceState>%(isInvoice)s</invoiceState>\
        <invoiceType>%(invoiceType)s</invoiceType>\
        <invoiceContent>1</invoiceContent>\
        <tradeNo>%(tradeNo)s</tradeNo>\
        <zip>210000</zip>\
        <remark>混合支付创建订单</remark>\
        <townId>%(townId)s</townId>\
        <companyCustNo>%(companyCustNo)s</companyCustNo>\
        %(skuInfo)s\
        <servFee>%(servFee)s</servFee>\
        <invoiceTitle>混合下单抬头</invoiceTitle>\
        <amount>%(amount)s</amount>\
        <email>yanhua@163.com</email>\
        <address>%(address)s</address>\
        <subPaymentModes>\
        <payAmount>%(7207)s</payAmount>\
        <payCode>7207</payCode>\
        </subPaymentModes>\
        <subPaymentModes>\
        <payAmount>%(7208)s</payAmount>\
        <payCode>7208</payCode>\
        </subPaymentModes>\
        <subPaymentModes>\
        <payAmount>%(7209)s</payAmount>\
        <payCode>7209</payCode>\
        </subPaymentModes>\
        <receiverName>段启阳</receiverName>\
        <telephone>010-84728989</telephone>\
        <specialVatTicket>\
        <taxNo>123456789012345</taxNo>\
        <regTel>15811084770</regTel>\
        <regAdd>%(address)s</regAdd>\
        <regAccount>23235254664336</regAccount>\
        <companyName>段启阳测试公司</companyName>\
        <regBank>混合银行</regBank>\
        <consigneeName>收票人姓名</consigneeName>\
        <consigneeAddress>收票人地址</consigneeAddress>\
        <consigneeMobileNum>16812291213</consigneeMobileNum>\
        </specialVatTicket>\
        <mobile>15812291213</mobile> \
        <hopeArrivalTime>%(hopeArrivalTime)s</hopeArrivalTime>\
        </addMixpayorder></sn_body></sn_request>"


    class MixPayOrder():
        method = "suning.govbus.mixconfirmorder.add"
        data = "<sn_request>\
        <sn_body>\
        <addMixconfirmorder>\
        %(payInfo)s\
        <orderId>%(orderId)s</orderId>\
        </addMixconfirmorder>\
        </sn_body>\
        </sn_request>"

    class UnPaidOrder():
        method = "suning.govbus.unpaidorder.cancel"
        data = "<sn_request><sn_body><cancelUnpaidorder><orderId>%(orderId)s</orderId></cancelUnpaidorder></sn_body></sn_request>"

    class CancleOrder():
        method = "suning.govbus.rejectorder.delete"
        data = "<sn_request><sn_body><deleteRejectOrder><orderId>%(orderId)s</orderId>\
        </deleteRejectOrder></sn_body></sn_request>"

    class CancleOrderEnd():
        method = "suning.govbus.applyrejected.add"
        data = "<sn_request><sn_body><addApplyRejected>%(skus)s\
        <orderId>%(orderId)s</orderId><bankName>%(bankName)s</bankName>\
        <cardUsername>%(cardUsername)s</cardUsername><cardNumber>%(cardNumber)s</cardNumber>\
        </addApplyRejected></sn_body></sn_request>"

    class ReturnPartOrder():
        method = "suning.govbus.returnpartorder.add"
        data = "<sn_request><sn_body><addReturnpartorder>%(skuIdinfo)s\
                <orderId>%(orderId)s</orderId><bankName>%(bankName)s</bankName>\
                <cardUsername>%(cardUsername)s</cardUsername><cardNumber>%(cardNumber)s</cardNumber><aftersalePhone>%(aftersalePhone)s</aftersalePhone><aftersaleName>%(aftersaleName)s</aftersaleName>\
                <aftersaleAddress><provinceId>%(provinceId)s</provinceId><cityId>%(cityId)s</cityId>\
                <countyId>%(countyId)s</countyId><townId>%(townId)s</townId><address>%(address)s</address>\
                </aftersaleAddress></addReturnpartorder></sn_body></sn_request>"

    class GetStatus():
        method = "suning.govbus.orderstatus.get"
        data = "<sn_request><sn_body><getOrderStatus><orderId>%(orderId)s</orderId></getOrderStatus></sn_body></sn_request>"

    class GetPeriodLimit():
        method = "suning.govbus.getperiodlimit.query"
        data = "<sn_request><sn_body><queryGetperiodlimit><userAccount>%(userAccount)s</userAccount></queryGetperiodlimit></sn_body></sn_request>"

    class GetBill():
        method = "suning.govbus.getbill.query"
        data = "<sn_request><sn_body><queryGetbill><pgSize>%(pgSize)s</pgSize><type>%(type)s</type><pageNum>%(pageNum)s</pageNum><info>%(info)s</info></queryGetbill></sn_body></sn_request>"

    class SearchProdExtend():
        method = "suning.govbus.prodextend.get"
        data = "<sn_request><sn_body><getProdextend><skus><price>0.00</price><skuId>%(skuId)s</skuId></skus></getProdextend></sn_body></sn_request>"

    class QueryProdExtend():
        method = "suning.govbus.aftersale.query"
        data = "<sn_request><sn_body><queryAftersale><skus><skuId>%(skuId)s</skuId></skus><cityId>%(cityId)s</cityId></queryAftersale></sn_body></sn_request>"


    class OrderDetail():
        method = "suning.govbus.orderdetail.get"
        data = "<sn_request><sn_body><getOrderDetail><orderId>%(orderId)s</orderId></getOrderDetail></sn_body></sn_request>"

    class QueryItemDetail():
        method = "suning.govbus.orderitemdetail.get"
        data = "<sn_request><sn_body><getOrderitemdetail>%(orderIds)s</getOrderitemdetail></sn_body></sn_request>"

    class QueryOrderAccount():
        method = "suning.govbus.orderaccount.query"
        data = "<sn_request><sn_body><queryOrderAccount><startDate>%(startDate)s</startDate>\
        <endDate>%(endDate)s</endDate><pageNo>%(pageNo)s</pageNo><pageSize>%(pageSize)s</pageSize>\
        <orderStatus>%(orderStatus)s</orderStatus></queryOrderAccount></sn_body></sn_request>"

    class QueryOrderItem():
        method = "suning.govbus.orderitem.query"
        data = "<sn_request><sn_body><queryOrderitem><startDate>%(startDate)s</startDate>\
        <orderItemStatus>%(orderItemStatus)s</orderItemStatus><companyCusNo>%(companyCusNo)s</companyCusNo>\
        <endDate>%(endDate)s</endDate><dateType>%(dateType)s</dateType><pageLen>%(pageLen)s</pageLen>\
        <pageNum>%(pageNum)s</pageNum></queryOrderitem></sn_body></sn_request>"

    class GetOrderLogist():
        method = "suning.govbus.orderlogist.get"
        data = "<sn_request><sn_body><getOrderLogist><orderId>%(orderId)s</orderId><orderItemId>%(orderItemId)s</orderItemId><skuId>%(skuId)s</skuId></getOrderLogist></sn_body></sn_request>"

    class Getlogistdetail():
        method = "suning.govbus.logistdetail.get"
        data = "<sn_request><sn_body><getLogistdetail><orderId>%(orderId)s</orderId><orderItemIds><orderItemId>%(orderItemId)s</orderItemId></orderItemIds></getLogistdetail></sn_body></sn_request>"

    class GetOrderLogistNew():
        method = "suning.govbus.orderlogistnew.get"
        data = "<sn_request><sn_body><getOrderlogistnew><orderId>%(orderId)s</orderId><orderItemIds><orderItemId>%(orderItemId)s</orderItemId><skuId>%(skuId)s</skuId></orderItemIds></getOrderlogistnew></sn_body></sn_request>"

    class GetShipTime():
        method = "suning.govbus.shiptime.get"
        data = "<sn_request><sn_body><getShipTime>%(skuIds)s\
                <cityId>%(cityId)s</cityId><districtId>%(districtId)s</districtId><townId>%(townId)s</townId>\
                <addrDetail>%(addrDetail)s</addrDetail></getShipTime></sn_body></sn_request>"
    class GetShipCarriage():
        method = "suning.govbus.shipcarriage.get"
        data = "<sn_request><sn_body><getShipCarriage><skuIds><skuId>%(skuId)s</skuId><piece>%(piece)s</piece></skuIds>\
                <cityId>%(cityId)s</cityId><districtId>%(districtId)s</districtId><townId>%(townId)s</townId>\
                <addrDetail>%(addrDetail)s</addrDetail></getShipCarriage></sn_body></sn_request>"

    class ConFacProduct():
        method = "suning.govbus.facproduct.confirm"
        data = "<sn_request><sn_body><confirmFacProduct><orderId>%(orderId)s</orderId>%(skuIdinfo)s</confirmFacProduct></sn_body></sn_request>"

    class EleInvoice():
        method = "suning.govbus.eleinvoice.get"
        data = "<sn_request><sn_body><getEleinvoice><orderItems><orderItemId>%(orderItemId)s</orderItemId><skuId>%(skuId)s</skuId></orderItems><orderId>%(orderId)s</orderId></getEleinvoice></sn_body></sn_request>"

    class GetInvoice():
        method = "suning.govbus.getinvoice.query"
        data = "<sn_request><sn_body><queryGetinvoice><field>%(field)s</field><type>%(type)s</type></queryGetinvoice></sn_body></sn_request>"

    class InvoiceLogistic():
        method = "suning.govbus.invoicelogist.get"
        data = "<sn_request><sn_body><getInvoicelogist><parameter>%(parameter)s</parameter><parameterInvoice>%(parameterInvoice)s</parameterInvoice><type>%(type)s</type><pageNum>%(pageNum)s</pageNum></getInvoicelogist></sn_body></sn_request>"

    class SignInvoice():
        method = "suning.govbus.signinvoice.query"
        data = "<sn_request><sn_body><querySigninvoice><parameter>%(parameter)s</parameter><confirmType>%(confirmType)s</confirmType></querySigninvoice></sn_body></sn_request>"

    class ConfirmInvoice():
        method = "suning.govbus.invoice.confirm"
        data = "<sn_request><sn_body><confirmInvoice>%(orderInfoDTO)s<applyForInvoiceReqDTO><invoiceType>%(invoiceType)s</invoiceType>\
        <invoiceContent>%(invoiceContent)s</invoiceContent><title>%(title)s</title><taxNo>%(taxNo)s</taxNo>\
        <regTel>%(regTel)s</regTel><companyName>%(companyName)s</companyName><regAdd>%(regAdd)s</regAdd>\
        <regBank>%(regBank)s</regBank><regAccount>%(regAccount)s</regAccount>\
        <consigneeName>%(consigneeName)s</consigneeName><consigneeMobileNum>%(consigneeMobileNum)s</consigneeMobileNum>\
        <address>%(address)s</address><markId>%(markId)s</markId></applyForInvoiceReqDTO></confirmInvoice></sn_body></sn_request>"

    class GetPicture():
        method = "suning.govbus.prodimage.query"
        data = "<sn_request><sn_body><queryProdImage>%(skuIds)s</queryProdImage></sn_body></sn_request>"

    class BatchStatus():
        method = "suning.govbus.batchprodsalestatus.get"
        data = "<sn_request><sn_body><getBatchProdSaleStatus>%(skuIds)s</getBatchProdSaleStatus></sn_body></sn_request>"

    class ProdReview():
        method = "suning.govbus.prodreview.query"
        data = "<sn_request><sn_body><queryProdReview>%(skuId)s</queryProdReview></sn_body></sn_request>"

    class CombinationProd():
        method = "suning.govbus.combinationprod.query"
        data = "<sn_request><sn_body><queryCombinationProd><skuId>%(skuId)s</skuId></queryCombinationProd></sn_body></sn_request>"

    class GetPictureDetail():
        method = "suning.govbus.proddetail.get"
        data = "<sn_request><sn_body><getProdDetail><skuId>%(skuId)s</skuId></getProdDetail></sn_body></sn_request>"

    class GetCategory():
        method = "suning.govbus.category.get"
        data = "<sn_request><sn_body><getCategory/></sn_body></sn_request>"

    class CategorySearch():
        method = "suning.govbus.categorysearch.query"
        data = "<sn_request><sn_body><queryCategorysearch><searchContent>%(keyword)s</searchContent></queryCategorysearch></sn_body></sn_request>"

    class ProductMapping():
        method = "suning.govbus.productmapping.query"
        data = "<sn_request><sn_body><queryProductmapping><currentPage>%(currentPage)s</currentPage></queryProductmapping></sn_body></sn_request>"

    class GetProductCluster():
        method = "suning.govbus.getproductcluster.get"
        data = "<sn_request><sn_body><getGetproductcluster><skuId>%(skuId)s</skuId></getGetproductcluster></sn_body></sn_request>"

    class GetMessage():
        method = "suning.govbus.message.get"
        data = "<sn_request><sn_body><getMessage><type>%(type)s</type></getMessage></sn_body></sn_request>"

    class SetSecretKey():
        method = "suning.govbus.setsecretkey.update"
        data = "<sn_request><sn_body><updateSetsecretkey><publicKey>%(publicKey)s</publicKey><type>%(type)s</type></updateSetsecretkey></sn_body></sn_request>"

    class GetCardSecretkey():
        method = "suning.govbus.getcardsecretkey.query"
        data = "<sn_request><sn_body><queryGetcardsecretkey><gcOrderNo>%(gcOrderNo)s</gcOrderNo><pageNumber>%(pageNumber)s</pageNumber><currentPage>%(currentPage)s</currentPage></queryGetcardsecretkey></sn_body></sn_request>"

    class QueryServicescheDule():
        method = "suning.govbus.serviceschedule.query"
        data = "<sn_request><sn_body><queryServiceschedule><orderId>%(orderId)s</orderId>%(orderItemIdsinfo)s<serviceType>%(serviceType)s</serviceType></queryServiceschedule></sn_body></sn_request>"


    class DeleteMessage():
        method = "suning.govbus.message.delete"
        data = "<sn_request><sn_body><deleteMessage><id>%(id)s</id></deleteMessage></sn_body></sn_request>"

    class GetServicerates():
        method = "suning.govbus.servicerates.get"
        data = "<sn_request><sn_body><getServicerates><orderId>%(orderId)s</orderId>%(orderItemIds)s</getServicerates></sn_body></sn_request>"

    class PreDepositBalance():
        method = "suning.govbus.predepositbalance.get"
        data = "<sn_request><sn_body><getPreDepositBalance/></sn_body></sn_request>"

    class CreateOnlinePay():
        method = "suning.govbus.onlinepay.create"
        data = "<sn_request><sn_body><createOnlinepay><orderId>%(orderId)s</orderId>\
                <channelType>%(channelType)s</channelType><backUrl>%(backUrl)s</backUrl>\
                </createOnlinepay></sn_body></sn_request>"

    class GetPriceMessage():
        method = "suning.govbus.pricemessage.query"
        data = "<sn_request><sn_body><queryPricemessage/></sn_body></sn_request>"

    class GetPaymentWay():
        method = "suning.govbus.paymentway.get"
        data = "<sn_request><sn_body><getPaymentway><provinceCode>%(provinceCode)s</provinceCode><cityCode>%(cityCode)s</cityCode><districtCode>%(districtCode)s</districtCode><townCode>%(townCode)s</townCode><skuId>%(skuId)s</skuId><payAmount>%(payAmount)s</payAmount></getPaymentway></sn_body></sn_request>"

    class GetfullAddress():
        method = "suning.govbus.fulladdress.get"
        data = "<sn_request><sn_body><getFullAddress/></sn_body></sn_request>"

    class JudgeFacProduct():
        method = "suning.govbus.judgefacproduct.get"
        data = "<sn_request><sn_body><getJudgefacproduct>%(skuIds)s<cityId>%(cityId)s</cityId></getJudgefacproduct></sn_body></sn_request>"

    class ProductSearch():
        method = "suning.govbus.productsearch.query"
        data = "<sn_request><sn_body><queryProductsearch><searchContent>%(searchContent)s</searchContent><cityCode>%(cityCode)s</cityCode><categoryIdOne>%(categoryIdOne)s</categoryIdOne><categoryIdTwo>%(categoryIdTwo)s</categoryIdTwo><categoryIdThree>%(categoryIdThree)s</categoryIdThree><min>%(min)s</min><max>%(max)s</max><sortType>%(sortType)s</sortType><page>%(page)s</page><limit>%(limit)s</limit><aggregate>%(aggregate)s</aggregate><attrList>%(attrList)s</attrList><brandId>%(brandId)s</brandId></queryProductsearch></sn_body></sn_request>"

    class GetPool():
        method = "suning.govbus.prodpool.query"
        data = "<sn_request><sn_body><queryProdPool><pgSize>%(pgSize)s</pgSize><pageNum>%(pageNum)s</pageNum><categoryId>%(categoryId)s</categoryId></queryProdPool></sn_body></sn_request>"

    class GetSpecialGoods():
        method = "suning.govbus.getspecialgoods.query"
        data = "<sn_request><sn_body><queryGetspecialgoods><pgSize>%(pgSize)s</pgSize><pageNum>%(pageNum)s</pageNum><categoryId>%(categoryId)s</categoryId></queryGetspecialgoods></sn_body></sn_request>"

    class LogNumSubmit():
        method = "suning.govbus.lognumsubmit.add"
        data = "<sn_request><sn_body><addLognumsubmit><orderId>%(orderId)s</orderId>%(orderItemIds)s<serviceType>%(serviceType)s</serviceType></addLognumsubmit></sn_body></sn_request>"

    class RepairMethodQuery():
        method = "suning.govbus.repairmethod.query"
        data = "<sn_request><sn_body><queryRepairmethod><orderId>%(orderId)s</orderId><orderItemId>%(orderItemId)s</orderItemId><skuId>%(skuId)s</skuId><cityId>%(cityId)s</cityId><countyId>%(countyId)s</countyId></queryRepairmethod></sn_body></sn_request>"

    class AfterServiceQuery():
        method = "suning.govbus.afterservice.query"
        data = "<sn_request><sn_body><queryAfterservice><orderId>%(orderId)s</orderId><cityId>%(cityId)s</cityId><countyId>%(countyId)s</countyId>%(skus)s</queryAfterservice></sn_body></sn_request>"

    class ApplyRepairGoods():
        method = "suning.govbus.applyrepairgoods.create"
        data = "<sn_request><sn_body><createApplyrepairgoods><orderId>%(orderId)s</orderId><orderItemId>%(orderItemId)s</orderItemId><skuId>%(skuId)s</skuId><num>%(num)s</num><serviceTime>%(serviceTime)s</serviceTime><receiverName>%(receiverName)s</receiverName><phoneNum>%(phoneNum)s</phoneNum><mobPhoneNum>%(mobPhoneNum)s</mobPhoneNum><srvMemo>%(srvMemo)s</srvMemo><orderMemo>%(orderMemo)s</orderMemo><provinceId>%(provinceId)s</provinceId><cityId>%(cityId)s</cityId><countyId>%(countyId)s</countyId><townId>%(townId)s</townId><address>%(address)s</address></createApplyrepairgoods></sn_body></sn_request>"

    class CancelRepairGoods():
        method = "suning.govbus.repairgoods.cancel"
        data = "<sn_request><sn_body><cancelRepairgoods><orderId>%(orderId)s</orderId><orderItemId>%(orderItemId)s</orderItemId><skuId>%(skuId)s</skuId><sheetId>%(sheetId)s</sheetId><cancelReason>%(cancelReason)s</cancelReason></cancelRepairgoods></sn_body></sn_request>"

    class ApplyexChangeGoods():
        method = "suning.govbus.applyexchangegoods.create"
        data = "<sn_request><sn_body><createApplyexchangegoods><orderId>%(orderId)s</orderId>%(orderItemIds)s</createApplyexchangegoods></sn_body></sn_request>"

    class CancelRetchgGoods():
        method = "suning.govbus.retchggoods.cancel"
        data = "<sn_request><sn_body><cancelRetchggoods><operateType>%(operateType)s</operateType><orderId>%(orderId)s</orderId><orderItems>%(orderItems)s</orderItems></cancelRetchggoods></sn_body></sn_request>"

    class AliPay():
        method = "suning.govbus.alipay.create"
        data = "<sn_request><sn_body><createAlipay><mobileOS>%(mobileOS)s</mobileOS><mobileModel>%(mobileModel)s</mobileModel><channelType>%(channelType)s</channelType><backUrl>%(backUrl)s</backUrl>%(orderId)s</createAlipay></sn_body></sn_request>"

    class BankTransfer():
        method = "suning.govbus.banktransfer.create"
        data = "<sn_request><sn_body><createBanktransfer><phoneNum>%(phoneNum)s</phoneNum>%(orderIds)s</createBanktransfer></sn_body></sn_request>"

    class SerialnoQuery():
        method = "suning.govbus.serialno.query"
        data = "<sn_request><sn_body><querySerialno><orderId>%(orderId)s</orderId><orderItemId>%(orderItemId)s</orderItemId><skuId>%(skuId)s</skuId></querySerialno></sn_body></sn_request>"


    class PoOrderId():
        method = "suning.govbus.poorderid.add"
        data = "<sn_request><sn_body><addPoorderid><orderId>%(orderId)s</orderId><porderId>%(porderId)s</porderId>%(skus)s</addPoorderid></sn_body></sn_request>"

    class poConfirm():
        method = "suning.govbus.poorder.confirm"
        data = "<sn_request><sn_body><confirmPoorder><orderId>%(orderId)s</orderId><poNumber>%(poNumber)s</poNumber>%(acLineList)s</confirmPoorder></sn_body></sn_request>"

    class Deleteinvoicebatch():
        method = "suning.govbus.invoicebatch.delete"
        data = "<sn_request><sn_body><deleteInvoicebatch>{}</deleteInvoicebatch></sn_body></sn_request>"

    class GetMarkIdInvoice():
        method = "suning.govbus.getmarkidinvoice.query"
        data = "<sn_request><sn_body><queryGetmarkidinvoice><markId>%(markId)s</markId><currentPage>%(currentPage)s</currentPage><pageNumber>%(pageNumber)s</pageNumber></queryGetmarkidinvoice></sn_body></sn_request>"

    class Getsubcodeproducts():
        method = "suning.govbus.subcodeproducts.get"
        data = "<sn_request><sn_body><getSubcodeproducts><generalSku>{}</generalSku></getSubcodeproducts></sn_body></sn_request>"

    class InvoiceSupplement():
        method = "suning.govbus.invoicesupplement.confirm"
        data = "<sn_request><sn_body><confirmInvoicesupplement>%(orderInfoDTO)s<applyForInvoiceReqDTO><regAccount>%(regAccount)s</regAccount><regTel>%(regTel)s</regTel><invoiceContent>%(invoiceContent)s</invoiceContent><address>%(address)s</address><markId>%(markId)s</markId><companyName>%(companyName)s</companyName><regAdd>%(regAdd)s</regAdd><remark>%(remark)s</remark><title>%(title)s</title><consigneeName>%(consigneeName)s</consigneeName><consigneeMobileNum>%(consigneeMobileNum)s</consigneeMobileNum><invoiceType>%(invoiceType)s</invoiceType><regBank>%(regBank)s</regBank><taxNo>%(taxNo)s</taxNo></applyForInvoiceReqDTO></confirmInvoicesupplement></sn_body></sn_request>"

    class Productareasalestatus():
        method = 'suning.govbus.productareasalestatus.query'
        data = "<sn_request><sn_body><queryProductareasalestatus><cityId>%(cityId)s</cityId>%(skuIds)s<provinceId>%(provinceId)s</provinceId></queryProductareasalestatus></sn_body></sn_request>"

    class Mixpayorder_NHXD():
        method = 'suning.govbus.mixpayorder.add'
        data = "<sn_request><sn_body><addMixpayorder>\
        <payment>%(payTpye)s</payment>\
        <orderType>%(orderType)s</orderType>\
        <provinceId>%(province)s</provinceId>\
        <cityId>%(city)s</cityId>\
        <countyId>%(county)s</countyId>\
        <invoiceState>%(isInvoice)s</invoiceState>\
        <invoiceType>%(invoiceType)s</invoiceType>\
        <invoiceContent>1</invoiceContent>\
        <tradeNo>%(tradeNo)s</tradeNo>\
        <zip>210000</zip>\
        <remark>混合支付创建订单</remark>\
        <townId>%(townId)s</townId>\
        <companyCustNo>%(companyCustNo)s</companyCustNo>\
        %(skuInfo)s\
        <servFee>%(servFee)s</servFee>\
        <invoiceTitle>混合下单抬头</invoiceTitle>\
        <amount>%(amount)s</amount>\
        <email>yanhua@163.com</email>\
        <address>%(address)s</address>\
        <subPaymentModes>\
        <payAmount>%(9005)s</payAmount>\
        <payCode>9005</payCode>\
        </subPaymentModes>\
        <subPaymentModes>\
        <payAmount>%(2931)s</payAmount>\
        <payCode>2931</payCode>\
        </subPaymentModes>\
        <receiverName>段启阳</receiverName>\
        <telephone>010-84728989</telephone>\
        <specialVatTicket>\
        <taxNo>123456789012345</taxNo>\
        <regTel>15811084770</regTel>\
        <regAdd>%(address)s</regAdd>\
        <regAccount>23235254664336</regAccount>\
        <companyName>段启阳测试公司</companyName>\
        <regBank>混合银行</regBank>\
        <consigneeName>收票人姓名</consigneeName>\
        <consigneeAddress>收票人地址</consigneeAddress>\
        <consigneeMobileNum>15812291213</consigneeMobileNum>\
        </specialVatTicket>\
        <mobile>15811084770</mobile> \
        <hopeArrivalTime>%(hopeArrivalTime)s</hopeArrivalTime>\
        </addMixpayorder></sn_body></sn_request>"

    class Mixpayorder_Alipay():
        method = 'suning.govbus.mixpayorder.add'
        data = "<sn_request><sn_body><addMixpayorder>\
        <payment>%(payTpye)s</payment>\
        <orderType>%(orderType)s</orderType>\
        <provinceId>%(province)s</provinceId>\
        <cityId>%(city)s</cityId>\
        <countyId>%(county)s</countyId>\
        <invoiceState>%(isInvoice)s</invoiceState>\
        <invoiceType>%(invoiceType)s</invoiceType>\
        <invoiceContent>1</invoiceContent>\
        <tradeNo>%(tradeNo)s</tradeNo>\
        <zip>210000</zip>\
        <remark>混合支付创建订单</remark>\
        <townId>%(townId)s</townId>\
        <companyCustNo>%(companyCustNo)s</companyCustNo>\
        %(skuInfo)s\
        <servFee>%(servFee)s</servFee>\
        <invoiceTitle>混合下单抬头</invoiceTitle>\
        <amount>%(amount)s</amount>\
        <email>yanhua@163.com</email>\
        <address>%(address)s</address>\
        <subPaymentModes>\
        <payAmount>%(9005)s</payAmount>\
        <payCode>9005</payCode>\
        </subPaymentModes>\
        <subPaymentModes>\
        <payAmount>%(4237)s</payAmount>\
        <payCode>4237</payCode>\
        </subPaymentModes>\
        <receiverName>段启阳</receiverName>\
        <telephone>010-84728989</telephone>\
        <specialVatTicket>\
        <taxNo>123456789012345</taxNo>\
        <regTel>15811084770</regTel>\
        <regAdd>%(address)s</regAdd>\
        <regAccount>23235254664336</regAccount>\
        <companyName>段启阳测试公司</companyName>\
        <regBank>混合银行</regBank>\
        <consigneeName>收票人姓名</consigneeName>\
        <consigneeAddress>收票人地址</consigneeAddress>\
        <consigneeMobileNum>15812291213</consigneeMobileNum>\
        </specialVatTicket>\
        <mobile>15811084770</mobile> \
        <hopeArrivalTime>%(hopeArrivalTime)s</hopeArrivalTime>\
        </addMixpayorder></sn_body></sn_request>"

    class Addabcpay():
        method = 'suning.govbus.abcpay.add'
        data = "<sn_request>\
                  <sn_body>\
                    <addAbcpay>\
                      <channelType>%(channelType)s</channelType>%(orderIdList)s\
                      <returnUrl>http://www.suning.com</returnUrl>\
                    </addAbcpay>\
                  </sn_body>\
                </sn_request>"

    class Cancelabcpay():
        method = 'suning.govbus.abcpay.cancel'
        data = "<sn_request>\
                  <sn_body>\
                    <cancelAbcpay>\
                      <orderId>%(orderId)s</orderId>\
                    </cancelAbcpay>\
                  </sn_body>\
                </sn_request>"

    class Individualeinvoice():
        method = 'suning.govbus.individualeinvoice.query'
        data = "<sn_request>\
                  <sn_body>\
                    <queryIndividualeinvoice>\
                      <gcOrderNo>%(gcOrderNo)s</gcOrderNo>\
                      <gcItemNo>%(gcItemNo)s</gcItemNo>\
                    </queryIndividualeinvoice>\
                  </sn_body>\
                </sn_request>"

    class Addindividualeinvoice():
        method = 'suning.govbus.individualeinvoice.add'
        data = "<sn_request>\
                  <sn_body>\
                    <addIndividualeinvoice>\
                      <gcItemNo>%(gcItemNo)s</gcItemNo>\
                      <companyName>%(companyName)</companyName>\
                      <contractMobile>%(contractMobile)</contractMobile>\
                      <znxbj>%(znxbj)s</znxbj>\
                      <remark>发票备注消息</remark>\
                    </addIndividualeinvoice>\
                  </sn_body>\
                </sn_request>"