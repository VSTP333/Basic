from ApiShopping.API.D0001_STANDAPI.Base import StandApi
envi = 'pre'
# appKey = 'f0b87e006b5352abfb368e9ed7312b23'
# appSecret = '8db1ceec63ae571e08d137ef3503f60f'
appKey = 'd0562c767ac7a7983d781062818175d1'
appSecret = 'fd9953b5c64d730fcda7834f939c6787'

api = StandApi(envi=envi, appKey=appKey, appSecret=appSecret,isLog='N')

# skus = '520001332,520001345'
# skus = '102473734'
skus = '102473734'
city = '025'
gcOrderNo = '100001863991'
##########商品类#############
# 获取商品目录=api.getCategory()
# 商品搜索=api.productSearch(searchContent='1',cityCode=city)
# 商品类目搜索=api.categorySearch(keyword='得力')
# 商品映射关系=api.productMapping(currentPage='1')
# 获取商品簇信息接口=api.getProductCluster(skuId=skus)
# 判断商品是否厂送 = api.judgeFacProduct(skuIds=skus, cityId=city)
# 查询商品扩展信息接口=api.searchProdExtend(skuId=skus)
# 查询商品扩展信息接口新=api.queryProdExtend(skuId=skus,cityId='025')
# 获取特殊商品池=api.getSpecialGoods(categoryId='198bc838-1db8-439f-a8c7-59fcc5a39e8b',pageNum='17',pgSize='1')
# 获取商品池商品=api.getPool(categoryId='A0101001',pageNum='1',pgSize='5')
# 查询商品详情=api.getPictureDetail(skuId=skus)
# 查询商品图片=api.getPicture(skuId=skus)
# 查询商品上下架状态=api.batchStatus(skuIds=skus,cityId='025')
# 获取商品评价=api.prodReview(skuIds=skus)
# 获取套餐清单=api.combinationProd(skuId=skus)
# 获取通子码商品信息接口 = api.getsubcodeproducts(generalSku='121344104')
# 商品可售状态查询接口 = api.productareasalestatus(skus='121347740,121347657,121347748',province='010',cityId='')
##########价格类#############
# 查询商品价格=api.getPrice(skuIds=skus,city=city)
##########库存类#############
# 查询单个精准库存=api.getInventory(skuIds=skus,city=city,num=4,countyId='01')
批量查询库存=api.getStock(skuIds=skus,city=city)
##########订单类#############
# 老创建订单=api.addOrder(orderType='0',payType="08",nums='10',invoiceType=1,invoiceState='0',skuIds=skus)
# 新创建订单=api.addMixOrder(orderType='0',payType='08',nums='5',invoiceType=2,isInvoice=0,skuIds=skus,isservFee='N')
# 新创建订单=api.addMixOrder(orderType='1',payType='08',nums='2',invoiceType=2,isInvoice=0,skuIds=skus,isservFee='N',province='9',city='73',county='759')
# 混合支付确认订单接口=api.mixPayOrder(orderId='100002015965')
# 取消预占库存订单=api.cancleOrder(orderId='100001839590')
# 未支付订单取消接口=api.unPaidOrder(orderId='100001819251')
# 退货申请接口=api.cancleOrderEnd(skuId=skus,orderId='100001535525',reason='0101',reasonDetails='不想要了',\
#                        bankName='03',cardUsername='王大力',cardNumber='6200121394857114')
# 部分退货接口=api.returnPartOrder(skuId=skus,num='1',orderId='100001825320',reason='0101',reasonDetails='不想要了',\
#                        bankName='03',cardUsername='王大力',cardNumber='6200121394857114')
# 获取订单状态接口=api.getStatus(orderId='100001535542')
# 查询订单详细信息=api.orderDetail(orderId='100001825320')
# 批量查询订单行接口=api.queryItemDetail(orderItem='10000151245001')
# 订单对账接口=api.queryOrderAccount(startDate="2019-03-01",endDate="2019-03-19")
# 订单行对账接口=api.queryOrderItem(startDate="2019-03-01",endDate="2019-03-15",orderItemStatus="4",companyCusNo='')
# 客户账期额度查询接口=api.getPeriodLimit(userAccount='19911010083@163.com')
# 获取账单信息接口=api.getBill(types='1',info='201911010030007378')
# 企业汇款支付=api.bankTransfer(phoneNum='',orderId='')
# 查询订单sn码=api.serialnoQuery(orderId='100001898246',orderItemId='10000189824601',skuId='102473734')
# po单提交接口=api.poOrderId(orderId='100001912555',porderId='202010000',orderItemId='10000191255501',skuId=skus,num='2',porderItemId='2020100001',remark='嘎嘎嘎')
# po单验收接口=api.poConfirm(orderId='100001912555',poNumber='202010000',orderItemId='10000191255501',poLineNumber='2020100001',poLineLocationId='1221221232',skuId=skus,quantity='2',confirmTime='2020-02-03 16:23:21')
##########售后类#############
# 售后进度查询接口=api.queryServicescheDule(orderId='100001492377',serviceType='1',orderItem='10000149237701',skuId='121307256')
# 维修方式查询接口=api.repairMethodQuery (orderId='',orderItemId='',skuId='',cityId='025',countyId='01')
# 售后服务类型查询接口=api.afterServiceQuery(orderId='100001496123',orderItemId='10000149612301',skuId='121347740',cityId='025',countyId='01')
# 维修申请接口 = api.applyRepairGoods(orderId='100001492377',orderItemId='10000149237701',skuId='121307256',serviceTime='20191118090000')
# 取消维修申请接口 = api.cancelRepairGoods(orderId='100001492377',orderItemId='10000149237701',skuId='121307256',sheetId='9020081713',cancelReason='不需要维修了')
# 换货申请接口 = api.applyexChangeGoods(orderId='100001821635',orderItemId='10000182163501',skuId=skus,num='3',reasonDetails='屏幕损坏')
# 厂送寄退物流提报接口=api.logNumSubmit(orderId='100001820008')
# 取消退换货接口 = api.cancelRetchgGoods(orderId='100001820008',orderItemId='10000182000801',skuId='121347746',operateType='1')
##########物流类#############
# 获取订单物流详情=api.getOrderLogist(orderId='100000016516',orderItemId='10000001651601',skuId='1620771420')
# 获取订单物流详情新=api.getOrderLogistNew(orderId='100001852608',orderItemId='10000185260801',skuId='121347746')
# 物流时效接口=api.getShipTime(skuId=skus,addrDetail="国宸餐饮")
# 物流运费接口=api.getShipCarriage(skuId=skus,cityId='',addrDetail="国宸餐饮")
# 厂送商品确认收货接口=api.conFacProduct(orderId='100000016516',skuId='620771420')
# 获取订单包裹信息=api.getLogistDetail(orderId='100001852608',orderItemId='10000185260801')
##########发票类#############
# 政企订单补开发票=api.confirmInvoice(gcOrderNo='100000016517',invoiceType=4,invoiceContent=1,\
#                             markId='BKFP202004200002',remark='补开电子发票')
# 电子发票查询接口=api.eleInvoice(orderId='100001444812',orderItemId='10000144481201',skuId=skus)
# 发票信息查询=api.getInvoice(field='100001539101',type='1')
# 发票签收接口 = api.signInvoice(parameter='100001839552',confirmType='1')
# 发票物流查询接口 = api.invoiceLogistic(parameter='2020050909057374',type='1',pageNum='1')
# 发票批次撤回接口 = api.deleteinvoicebatch(markIds="xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000,xxx1000000")
# 发票批次查询接口 = api.getMarkIdInvoice(markId='2020050909057374')
# 补开发票接口新 = api.invoiceSupplement(gcOrderNo='100001839742,100001839742') # 缺点，gcOrderNo的数量要比gcItemNo的数量大。否则会报错。
##########其他类#############
# 全量地址接口=api.getFullAddress()
# 是否支持货到付款接口=api.getPaymentWay(skuId='121347590')
# 价格变动消息查询接口=api.getPriceMessage()
# 在线支付接口=api.createOnlinePay(orderId='100001820669',payway='01')
# 支付宝支付接口=api.aliPay(orderId='100001824719',channelType='WAP')
# 查询预存款金额接口=api.preDepositBalance()
# 查询消息=api.getMessage(type=13)
# 删除消息接口=api.deleteMessage(id='98805598')
# 服务状态查询=api.getServiceRates(orderId='100001457192',orderItemId='')
# 设置公钥信息接口=api.setSecretKey(publicKey='',type='')
# 在线获取礼品卡卡密接口=api.getCardSecretKey(orderId='')
########################农行小豆##########################
# 农行小豆创单 = api.mixOrder_NHXD(orderType='1',nums='10',invoiceType=2,isInvoice=0,skuIds=skus,isservFee='N')
# 快E付支付 = api.addabcpay("100002016488,121344444")
# 快E付退款 = api.cancelabcpay(orderId='100002016488')
# 混合支付个人部分电子发票申请接口 = api.addindividualeinvoice(znxbj='1',gcItemNo='10000201648801')
# 混合支付个人部分电子发票查询接口 = api.individualeinvoice(gcOrderNo='100002016488',gcItemNo='10000201648801')