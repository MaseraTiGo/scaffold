# coding=UTF-8


from infrastructure.core.field.base import CharField, DictField, ListField, \
    IntField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.wechat.manager.api import WechatAuthorizedApi
from abs.middleground.business.person.manager import PersonServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from infrastructure.core.exception.business_error import BusinessError
from abs.services.agent.order.manager import OrderServer, OrderItemServer
from abs.services.agent.goods.manager import GoodsServer
from abs.middleground.business.order.manager import OrderServer as mg_OrderServer
from abs.services.crm.university.manager import UniversityServer, UniversityYearsServer
from abs.middleground.business.production.manager import ProductionServer
from abs.middleware.pay import pay_middleware
from abs.services.agent.customer.manager import AgentCustomerServer, SaleChanceServer
from abs.services.crm.agent.manager import AgentServer
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.middleware.extend.yunaccount import yunaccount_extend
from abs.services.agent.goods.manager import PosterServer
from abs.services.agent.event.manager import StaffOrderEventServer
from abs.services.customer.account.manager import CustomerAccountServer, TripartiteServer
from abs.services.customer.account.utils.constant import CategoryTypes
from abs.middleground.business.transaction.utils.constant import PayTypes
from abs.services.agent.order.utils.constant import OrderSource


class Add(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_info = RequestField(
        DictField,
        desc = "订单详情",
        conf = {
            'strike_price': IntField(desc = "金额"),
            'address_id': IntField(desc = "收货地址id", is_required = False),
            'invoice_info': DictField(
                desc="合同信息",
                is_required=False,
                conf={
                    'name': CharField(desc="名称"),
                    'phone': CharField(desc="电话"),
                    'identification': CharField(desc="身份证")
                }
            ),
            'goods_list': ListField(
                desc = '商品列表',
                fmt = DictField(
                    desc = '商品信息',
                    conf = {
                        'quantity': IntField(desc = "购买数量"),
                        'specification_id': IntField(desc = "规格id")
                    }
                )
            )
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.order_id = ResponseField(IntField, desc = "订单id")

    @classmethod
    def get_desc(cls):
        return "客户下单接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        order_info = request.order_info
        customer = self.auth_user
        invoice_info = {}
        if 'address_id' in order_info:
            address = PersonServer.get_address(order_info.pop('address_id'))
            invoice_info.update({
                'name': address.contacts,
                'phone': address.phone,
                'address': '-'.join([address.city, address.address])
            })
        if 'invoice_info' in order_info:
            invoice_info.update(order_info.pop('invoice_info'))
            flag, result = yunaccount_extend.verify_identity(
                invoice_info['name'],
                invoice_info['identification']
            )
            if not flag:
                raise BusinessError('姓名与身份证号不匹配')
        if not invoice_info:
            raise BusinessError('请填写发货信息')
        specification_list = []
        for goods_info in order_info['goods_list']:
            specification = MerchandiseServer.get_specification(goods_info['specification_id'])
            if specification.stock < goods_info['quantity']:
                raise BusinessError('库存不足')
            if specification.merchandise.use_status != 'enable':
                raise BusinessError('商品已下架')
            specification.order_count = goods_info['quantity']
            specification.total_price = goods_info['quantity'] * specification.sale_price
            specification.production_id = specification.merchandise.production_id
            specification_list.append(specification)
        if not specification_list:
            raise BusinessError('请选择商品')
        GoodsServer.hung_goods([
            specification.merchandise
            for specification in specification_list]
        )
        UniversityServer.hung_school([
            specification.merchandise.goods
            for specification in specification_list]
        )
        UniversityServer.hung_major([
            specification.merchandise.goods
            for specification in specification_list]
        )
        ProductionServer.hung_production([
            specification
            for specification in specification_list
        ])
        UniversityYearsServer.hung_years([
            specification.merchandise.goods
            for specification in specification_list
        ])
        agent = AgentServer.get(specification_list[0].merchandise.goods.agent_id)

        agent_customer = AgentCustomerServer.create_foradd_order(
            customer,
            agent
        )
        agent_customer.agent = agent
        order = OrderServer.add(
            agent_customer,
            invoice_info,
            OrderSource.WECHAT,
            order_info['strike_price'],
            specification_list
        )
        SaleChanceServer.create_foradd_order(
            agent_customer,
            order.id
        )

        return order

    def fill(self, response, order):
        response.order_id = order.id
        return response


class PosterAdd(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.poster_id = RequestField(
        IntField,
        desc="海报id"
    )
    request.order_info = RequestField(
        DictField,
        desc = "订单详情",
        conf = {
            'strike_price': IntField(desc = "金额"),
            'address_id': IntField(desc = "收货地址id", is_required = False),
            'invoice_info': DictField(
                desc="合同信息",
                is_required=False,
                conf={
                    'name': CharField(desc="名称"),
                    'phone': CharField(desc="电话"),
                    'identification': CharField(desc="身份证")
                }
            ),
            'goods_list': ListField(
                desc = '商品列表',
                fmt = DictField(
                    desc = '商品信息',
                    conf = {
                        'quantity': IntField(desc = "购买数量"),
                        'specification_id': IntField(desc = "规格id")
                    }
                )
            )
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.order_id = ResponseField(IntField, desc = "订单id")

    @classmethod
    def get_desc(cls):
        return "客户海报下单接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        poster = PosterServer.get(request.poster_id)
        order_info = request.order_info
        customer = self.auth_user
        invoice_info = {}
        if 'address_id' in order_info:
            address = PersonServer.get_address(order_info.pop('address_id'))
            invoice_info.update({
                'name': address.contacts,
                'phone': address.phone,
                'address': '-'.join([address.city, address.address])
            })
        if 'invoice_info' in order_info:
            invoice_info.update(order_info.pop('invoice_info'))
            flag, result = yunaccount_extend.verify_identity(
                invoice_info['name'],
                invoice_info['identification']
            )
            if not flag:
                raise BusinessError('姓名与身份证号不匹配')
        if not invoice_info:
            raise BusinessError('请填写发货信息')
        specification_list = []
        for goods_info in order_info['goods_list']:
            specification = MerchandiseServer.get_specification(goods_info['specification_id'])
            if specification.stock < goods_info['quantity']:
                raise BusinessError('库存不足')
            if specification.merchandise.use_status != 'enable':
                raise BusinessError('商品已下架')
            specification.order_count = goods_info['quantity']
            specification.total_price = goods_info['quantity'] * specification.sale_price
            specification.production_id = specification.merchandise.production_id
            specification_list.append(specification)
        if not specification_list:
            raise BusinessError('请选择商品')
        GoodsServer.hung_goods([
            specification.merchandise
            for specification in specification_list]
        )
        for specification in specification_list:
            if specification.merchandise.goods.id != poster.goods.id:
                raise BusinessError('购买商品非海报商品')
        UniversityServer.hung_school([
            specification.merchandise.goods
            for specification in specification_list]
        )
        UniversityServer.hung_major([
            specification.merchandise.goods
            for specification in specification_list]
        )
        ProductionServer.hung_production([
            specification
            for specification in specification_list
        ])
        UniversityYearsServer.hung_years([
            specification.merchandise.goods
            for specification in specification_list
        ])
        agent = AgentServer.get(specification_list[0].merchandise.goods.agent_id)

        agent_customer = AgentCustomerServer.create_foradd_order(
            customer,
            agent
        )
        agent_customer.agent = agent
        order = OrderServer.add(
            agent_customer,
            invoice_info,
            'app',
            order_info['strike_price'],
            specification_list
        )
        SaleChanceServer.create_foradd_order(
            agent_customer,
            order.id
        )
        # todo 获取员工部门
        StaffOrderEventServer.create(
            order_id=order.id,
            staff_id=poster.staff_id,
            organization_id=1
        )
        return order

    def fill(self, response, order):
        response.order_id = order.id
        return response


class Get(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc = "订单id")

    response = with_metaclass(ResponseFieldSet)
    response.order_info = ResponseField(DictField, desc = "订单信息", conf = {
        'id': IntField(desc = "订单id"),
        'number': CharField(desc = "订单编号"),
        'status': CharField(desc = "订单状态"),
        'status_name': CharField(desc = "订单状态"),
        'strike_price': IntField(desc = "价格"),
        'create_time': DatetimeField(desc = "下单时间"),
        'last_payment_type': CharField(desc = '付款方式'),
        'last_payment_time': DatetimeField(desc = "付款时间"),
        'last_payment_number': CharField(desc = "最后付款单号"),
        'despatch_type': CharField(desc = "发货方式"),
        'order_item_list': ListField(
            desc = "商品列表",
            fmt = DictField(
                desc = "商品",
                conf = {
                    'id': IntField(desc = "订单商品详情id"),
                    'agent_name': CharField(desc="代理商"),
                    'sale_price': IntField(desc = "单价"),
                    'total_price': IntField(desc = "总价"),
                    'quantity': IntField(desc = "数量"),
                    'show_image': CharField(desc = "展示图片"),
                    'title': CharField(desc = "标题"),
                    'school_name': CharField(desc = "学校名称"),
                    'major_name': CharField(desc = "专业名称"),
                    'duration': CharField(desc = "学年"),
                    'category': CharField(desc="类别"),
                    'school_city': CharField(desc = "学校城市"),
                    'brand_name': CharField(desc = "品牌"),
                    'production_name': CharField(desc = "产品名"),
                    'remark': CharField(desc = "备注")
                }
            )
        ),
        'invoice_info': DictField(
            desc="发货信息",
            conf={
                'name': CharField(desc="姓名"),
                'phone': CharField(desc="手机号"),
                'address': CharField(desc="地址"),
                'identification': CharField(desc="身份证号")
            }
        )
    })

    @classmethod
    def get_desc(cls):
        return "订单详情"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        order = OrderServer.get(request.order_id)
        if order.person_id != self.auth_user.person_id:
            raise BusinessError('订单异常')
        order.order_item_list = OrderItemServer.search_all(order = order)
        mg_OrderServer.hung_snapshoot(order.order_item_list)
        AgentServer.hung_agent([order])
        return order

    def fill(self, response, order):
        response.order_info = {
            'id': order.id,
            'number': order.mg_order.number,
            'status': order.mg_order.status,
            'status_name': order.mg_order.get_status_display(),
            'strike_price': order.mg_order.strike_price,
            'create_time': order.mg_order.create_time,
            'last_payment_type': order.mg_order.payment.last_payment_type,
            'last_payment_time': order.mg_order.payment.last_payment_time,
            'last_payment_number': '',
            'despatch_type': order.order_item_list[0].snapshoot.despatch_type,
            'order_item_list': [{
                'id': order_item.id,
                'agent_name': order.agent.name,
                'sale_price': order_item.snapshoot.sale_price,
                'total_price': order_item.snapshoot.total_price,
                'quantity': order_item.snapshoot.count,
                'show_image': order_item.snapshoot.show_image,
                'title': order_item.snapshoot.title,
                'school_name': order_item.school_name,
                'major_name': order_item.major_name,
                'duration': order_item.get_duration_display(),
                'category': order_item.get_category_display(),
                'school_city': order_item.school_city,
                'brand_name': order_item.snapshoot.brand_name,
                'production_name': order_item.snapshoot.production_name,
                'remark': order_item.snapshoot.remark
            } for order_item in order.order_item_list],
            'invoice_info': {
                'name': order.mg_order.invoice.name,
                'phone': order.mg_order.invoice.phone,
                'address': order.mg_order.invoice.address,
                'identification': order.mg_order.invoice.identification
            }
        }
        return response


class Search(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页码")
    request.search_info = RequestField(
        DictField,
        desc = "搜索订单",
        conf = {
            'status': CharField(desc = "订单状态", is_required = False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "订单列表",
        fmt = DictField(
            desc = "订单信息",
            conf = {
                'id': IntField(desc = "订单id"),
                'number': CharField(desc = "订单编号"),
                'status': CharField(desc = "订单状态"),
                'status_name': CharField(desc = "订单状态"),
                'strike_price': IntField(desc = "价格"),
                'create_time': DatetimeField(desc = "下单时间"),
                'last_payment_type': CharField(desc = '付款方式'),
                'last_payment_time': CharField(desc = "付款时间"),
                'last_payment_number': CharField(desc = "最后付款单号"),
                'despatch_type': CharField(desc = "发货类型"),
                'order_item_list': ListField(
                    desc = "商品列表",
                    fmt = DictField(
                        desc = "商品",
                        conf = {
                            'agent_name': CharField(desc="代理商名称"),
                            'sale_price': IntField(desc = "单价"),
                            'total_price': IntField(desc = "总价"),
                            'quantity': IntField(desc = "数量"),
                            'show_image': CharField(desc = "展示图片"),
                            'title': CharField(desc = "标题"),
                            'school_name': CharField(desc = "学校名称"),
                            'major_name': CharField(desc = "专业名称"),
                            'duration': CharField(desc = "学年"),
                            'category': CharField(desc="类别"),
                            'school_city': CharField(desc = "学校城市"),
                            'brand_name': CharField(desc = "品牌"),
                            'production_name': CharField(desc = "产品名")
                        }
                    )
                ),
                'invoice_info': DictField(
                    desc="发货信息",
                    conf={
                        'name': CharField(desc="姓名"),
                        'phone': CharField(desc="手机号"),
                        'address': CharField(desc="地址"),
                        'identification': CharField(desc="身份证号")
                    }
                )
            }
        )
    )
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "订单列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        OrderServer.auto_cancel()
        page_list = OrderServer.search(
            request.current_page,
            person_id = self.auth_user.person_id,
            **request.search_info)
        OrderItemServer.hung_order_item(page_list.data)
        all_order_item_list = []
        for order in page_list.data:
            all_order_item_list.extend(order.orderitem_list)
        mg_OrderServer.hung_snapshoot(all_order_item_list)
        AgentServer.hung_agent(page_list.data)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': order.id,
            'number': order.mg_order.number,
            'status': order.mg_order.status,
            'status_name': order.mg_order.get_status_display(),
            'strike_price': order.mg_order.strike_price,
            'create_time': order.mg_order.create_time,
            'last_payment_type': order.mg_order.payment.last_payment_type,
            'last_payment_time': order.mg_order.payment.last_payment_time,
            'last_payment_number': '',
            'despatch_type': order.orderitem_list[0].snapshoot.despatch_type,
            'order_item_list': [{
                'agent_name': order.agent.name,
                'sale_price': order_item.snapshoot.sale_price,
                'total_price': order_item.snapshoot.total_price,
                'quantity': order_item.snapshoot.count,
                'show_image': order_item.snapshoot.show_image,
                'title': order_item.snapshoot.title,
                'school_name': order_item.school_name,
                'major_name': order_item.major_name,
                'duration': order_item.get_duration_display(),
                'category': order_item.get_category_display(),
                'school_city': order_item.school_city,
                'brand_name': order_item.snapshoot.brand_name,
                'production_name': order_item.snapshoot.production_name
            } for order_item in order.orderitem_list],
            'invoice_info': {
                'name': order.mg_order.invoice.name,
                'phone': order.mg_order.invoice.phone,
                'address': order.mg_order.invoice.address,
                'identification': order.mg_order.invoice.identification
            }
        } for order in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Pay(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc = "订单id")

    response = with_metaclass(ResponseFieldSet)
    response.pay_info = ResponseField(DictField, desc = '支付信息', conf = {
        'timestamp': CharField(desc = "时间"),
        'package': CharField(desc = "微信预支付id"),
        'noncestr': CharField(desc = "随机字符串"),
        'sign': CharField(desc = "签名")
    })

    @classmethod
    def get_desc(cls):
        return "付款"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        order = OrderServer.get(request.order_id)
        if order.status != OrderStatus.ORDER_LAUNCHED:
            raise BusinessError('订单状态异常，待支付订单才能付款')
        account = CustomerAccountServer.get(self.auth_user.id)
        if not account:
            raise BusinessError('账号异常')
        tripartite = TripartiteServer.search_all(
            customer_account=account,
            category=CategoryTypes.WECHAT
        ).first()
        if not tripartite:
            raise BusinessError('账号异常')
        prepay_id = OrderServer.pay(
            order,
            PayTypes.WECHAT,
            'JSAPI',
            openid=tripartite.openid
        )
        if not prepay_id:
            raise BusinessError('付款失败')
        pay_info = pay_middleware.parse_mini_pay_info(prepay_id)
        return pay_info

    def fill(self, response, pay_info):
        response.pay_info = {
            'timestamp': pay_info.get('timeStamp'),
            'package': pay_info.get('package'),
            'noncestr': pay_info.get('nonceStr'),
            'sign': pay_info.get('paySign')
        }
        return response


class Cancel(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc = "订单id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "取消订单"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        order = OrderServer.get(request.order_id)
        if order.person_id != self.auth_user.person_id:
            raise BusinessError('没有权限取消该订单')
        if order.mg_order.status != OrderStatus.ORDER_LAUNCHED:
            raise BusinessError('待付款订单才能取消')
        OrderServer.cancel(order)

    def fill(self, response):
        return response
