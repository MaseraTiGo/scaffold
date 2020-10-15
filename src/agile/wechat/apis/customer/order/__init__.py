# coding=UTF-8
import datetime
import json
from infrastructure.core.field.base import CharField, DictField, ListField, \
    IntField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.wechat.manager.api import WechatAuthorizedApi
from abs.middleground.business.person.manager import PersonServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from infrastructure.core.exception.business_error import BusinessError
from abs.services.agent.order.manager import OrderServer, OrderItemServer, \
     ContractServer, OrderPlanServer
from abs.services.agent.goods.manager import GoodsServer
from abs.middleground.business.order.manager import OrderServer as mg_OrderServer
from abs.services.crm.university.manager import UniversityServer, UniversityYearsServer
from abs.middleground.business.production.manager import ProductionServer
from abs.middleware.pay import pay_middleware
from abs.services.agent.customer.manager import AgentCustomerServer, SaleChanceServer
from abs.services.agent.agent.manager import AgentServer
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.middleware.extend.yunaccount import yunaccount_extend
from abs.services.agent.goods.manager import PosterServer
from abs.services.agent.event.manager import StaffOrderEventServer
from abs.services.customer.account.manager import CustomerAccountServer, TripartiteServer
from abs.services.customer.account.utils.constant import CategoryTypes
from abs.middleground.business.transaction.utils.constant import PayService
from abs.middleground.business.transaction.utils.constant import PayTypes
from abs.services.agent.order.utils.constant import OrderSource
from abs.middleground.business.merchandise.utils.constant import UseStatus
from abs.services.agent.order.manager import OrderItemEvaluationServer
from abs.services.agent.order.utils.constant import EvaluationTypes


class Add(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_info = RequestField(
        DictField,
        desc = "订单详情",
        conf = {
            'strike_price': IntField(desc = "金额"),
            'address_id': IntField(desc = "收货地址id", is_required = False),
            'invoice_info': DictField(
                desc = "合同信息",
                is_required = False,
                conf = {
                    'name': CharField(desc = "名称"),
                    'phone': CharField(desc = "电话"),
                    'identification': CharField(desc = "身份证")
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
            if specification.merchandise.use_status != UseStatus.ENABLE:
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
            order_info['strike_price'],
            PayService.FULL_PAYMENT,
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
        desc = "海报id"
    )
    request.order_info = RequestField(
        DictField,
        desc = "订单详情",
        conf = {
            'deposit': IntField(desc = "首付款金额"),
            'strike_price': IntField(desc = "成交价金额"),
            'address_id': IntField(desc = "收货地址id", is_required = False),
            'invoice_info': DictField(
                desc = "合同信息",
                is_required = False,
                conf = {
                    'name': CharField(desc = "名称"),
                    'phone': CharField(desc = "电话"),
                    'identification': CharField(desc = "身份证")
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
        if poster.expire_date < datetime.date.today():
            raise BusinessError('海报已过期')
        customer = self.auth_user
        person = PersonServer.get(customer.person_id)
        if not person or person.phone != poster.phone:
            raise BusinessError('专属二维码，您无权限扫码')
        order_info = request.order_info
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
        poster_specification_mapping = {}
        for poster_specification in poster.poster_specification_list:
            if poster_specification.specification_id not in poster_specification_mapping:
                poster_specification_mapping[poster_specification.specification_id] = poster_specification
        specification_list = []
        for goods_info in order_info['goods_list']:
            specification = MerchandiseServer.get_specification(goods_info['specification_id'])
            if specification.stock < goods_info['quantity']:
                raise BusinessError('库存不足')
            if specification.merchandise.use_status != UseStatus.ENABLE:
                raise BusinessError('商品已下架')
            specification.sale_price = poster_specification_mapping[specification.id].original_price
            specification.order_count = goods_info['quantity']
            specification.total_price = goods_info['quantity'] * \
                    specification.sale_price
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
            OrderSource.WECHAT,
            order_info['deposit'],
            order_info['strike_price'],
            poster.pay_services,
            specification_list
        )
        SaleChanceServer.create_foradd_order(
            agent_customer,
            order.id
        )
        # todo 获取员工部门
        StaffOrderEventServer.create(
            order_id = order.id,
            staff_id = poster.staff_id,
            organization_id = 1
        )
        # 添加回款计划
        plan_list = json.loads(poster.pay_plan)
        if len(plan_list) > 0:
            OrderPlanServer.batch_create(
                order,
                poster.staff_id,
                plan_list
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
        'sale_price': IntField(desc = "销售总金额"),
        'strike_price': IntField(desc = "成交金额"),
        'discount': IntField(desc = "优惠金额"),
        'deposit': IntField(desc = "需付款金额"),
        'arrears': IntField(desc = "欠费金额"),
        'actual_amount': IntField(desc = "实际支付金额"),
        'create_time': DatetimeField(desc = "下单时间"),
        'last_payment_type': CharField(desc = '付款方式'),
        'last_payment_time': DatetimeField(desc = "付款时间"),
        'last_payment_number': CharField(desc = "最后付款单号"),
        'last_payment_amount': IntField(desc = "最后支付金额"),
        'pay_services': CharField(desc = "订单支付服务"),
        'order_item_list': ListField(
            desc = "商品列表",
            fmt = DictField(
                desc = "商品",
                conf = {
                    'order_item_id': IntField(desc = "订单商品详情id"),
                    'goods_id': IntField(desc = "订单商品id"),
                    'evaluation': CharField(desc = "评价状态",
                                            choices=EvaluationTypes.CHOICES),
                    'agent_name': CharField(desc = "代理商"),
                    'sale_price': IntField(desc = "单价"),
                    'total_price': IntField(desc = "总价"),
                    'quantity': IntField(desc = "数量"),
                    'show_image': CharField(desc = "展示图片"),
                    'title': CharField(desc = "标题"),
                    'school_name': CharField(desc = "学校名称"),
                    'major_name': CharField(desc = "专业名称"),
                    'duration': CharField(desc = "学年"),
                    'category': CharField(desc = "类别"),
                    'school_city': CharField(desc = "学校城市"),
                    'brand_name': CharField(desc = "品牌"),
                    'production_name': CharField(desc = "产品名"),
                    'remark': CharField(desc = "备注"),
                    'despatch_type': CharField(desc = "发货方式"),
                    'contract_id': IntField(desc = "合同id"),
                    'contract_status': CharField(desc = "合同状态"),
                }
            )
        ),
        'invoice_info': DictField(
            desc = "发货信息",
            conf = {
                'name': CharField(desc = "姓名"),
                'phone': CharField(desc = "手机号"),
                'address': CharField(desc = "地址"),
                'identification': CharField(desc = "身份证号")
            }
        ),
       'payment_list': ListField(
            desc = "支付列表",
            fmt = DictField(
                desc = "支付详情",
                conf = {
                    'id': IntField(desc = "id"),
                    'amount': CharField(desc = "支付金额"),
                    'pay_type': CharField(desc = "支付方式"),
                    'status': CharField(desc = "支付状态"),
                    'number': CharField(desc = "支付单号"),
                    'create_time':  DatetimeField(desc = "支付时间"),
                }
            )
        ),
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
        ContractServer.hung_contract_byitem(order.order_item_list)
        AgentServer.hung_agent([order])
        return order

    def fill(self, response, order):
        response.order_info = {
            'id': order.id,
            'number': order.mg_order.number,
            'status': order.mg_order.status,
            'status_name': order.mg_order.get_status_display(),
            'sale_price': order.mg_order.requirement.sale_price,
            'strike_price':order.mg_order.strike_price,
            'discount': order.mg_order.requirement.sale_price - \
                        order.mg_order.strike_price,
            'deposit':order.deposit,
            'arrears': order.mg_order.strike_price - \
                       order.mg_order.payment.actual_amount,
            'actual_amount':order.mg_order.payment.actual_amount,
            'create_time': order.mg_order.create_time,
            'last_payment_type': order.mg_order.payment.last_payment_type,
            'last_payment_time': order.mg_order.payment.last_payment_time,
            'last_payment_number': '',
            'last_payment_amount':order.mg_order.payment.last_payment_amount,
            'pay_services':order.get_pay_services_display(),
            'payment_id':order.mg_order.payment.id,
            'order_item_list': [{
                'order_item_id': order_item.id,
                'goods_id': order_item.goods_id,
                'evaluation': order_item.evaluation,
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
                'remark': order_item.snapshoot.remark,
                'despatch_type': order_item.snapshoot.despatch_type,
                'contract_id': order_item.contract.id if \
                               order_item.contract else 0,
                'contract_status': order_item.contract.status if \
                                   order_item.contract else "",
            } for order_item in order.order_item_list],
            'invoice_info': {
                'name': order.mg_order.invoice.name,
                'phone': order.mg_order.invoice.phone,
                'address': order.mg_order.invoice.address,
                'identification': order.mg_order.invoice.identification
            },
           'payment_list': [{
                'id': payment_record.id,
                'amount': payment_record.amount,
                'pay_type': payment_record.get_pay_type_display(),
                'status': payment_record.get_status_display(),
                'number': "",
                'create_time': payment_record.create_time,
            } for payment_record in order.mg_order.payment.payment_list],
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
                'sale_price': IntField(desc = "销售总金额"),
                'strike_price': IntField(desc = "成交金额"),
                'discount': IntField(desc = "优惠金额"),
                'deposit': IntField(desc = "需付款金额"),
                'arrears': IntField(desc = "欠费金额"),
                'actual_amount': IntField(desc = "实际支付金额"),
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
                            'order_item_id': IntField(desc = "订单详情id"),
                            'goods_id': IntField(desc = "订单商品id"),
                            'evaluation': CharField(desc = "评价状态",
                                                    choices=EvaluationTypes.CHOICES),
                            'agent_name': CharField(desc = "代理商名称"),
                            'sale_price': IntField(desc = "单价"),
                            'total_price': IntField(desc = "总价"),
                            'quantity': IntField(desc = "数量"),
                            'show_image': CharField(desc = "展示图片"),
                            'title': CharField(desc = "标题"),
                            'school_name': CharField(desc = "学校名称"),
                            'major_name': CharField(desc = "专业名称"),
                            'duration': CharField(desc = "学年"),
                            'category': CharField(desc = "类别"),
                            'school_city': CharField(desc = "学校城市"),
                            'brand_name': CharField(desc = "品牌"),
                            'production_name': CharField(desc = "产品名"),
                            'contract_id': IntField(desc = "合同id"),
                            'contract_status': CharField(desc = "合同状态"),
                        }
                    )
                ),
                'invoice_info': DictField(
                    desc = "发货信息",
                    conf = {
                        'name': CharField(desc = "姓名"),
                        'phone': CharField(desc = "手机号"),
                        'address': CharField(desc = "地址"),
                        'identification': CharField(desc = "身份证号")
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
        ContractServer.hung_contract_byitem(all_order_item_list)
        AgentServer.hung_agent(page_list.data)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': order.id,
            'number': order.mg_order.number,
            'status': order.mg_order.status,
            'status_name': order.mg_order.get_status_display(),
            'sale_price': order.mg_order.requirement.sale_price,
            'strike_price':order.mg_order.strike_price,
            'discount': order.mg_order.requirement.sale_price - \
                        order.mg_order.strike_price,
            'deposit':order.deposit,
            'arrears': order.mg_order.strike_price - \
                       order.mg_order.payment.actual_amount,
            'actual_amount':order.mg_order.payment.actual_amount,
            'create_time': order.mg_order.create_time,
            'last_payment_type': order.mg_order.payment.last_payment_type,
            'last_payment_time': order.mg_order.payment.last_payment_time,
            'last_payment_number': '',
            'despatch_type': order.orderitem_list[0].snapshoot.despatch_type,
            'order_item_list': [{
                'order_item_id': order_item.id,
                'goods_id': order_item.goods_id,
                'evaluation': order_item.evaluation,
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
                'contract_id':order_item.contract.id if order_item.contract else 0,
                'contract_status': order_item.contract.status if order_item.contract else "",
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
            customer_account = account,
            category = CategoryTypes.WECHAT
        ).first()
        if not tripartite:
            raise BusinessError('账号异常')
        prepay_id = OrderServer.pay(
            order,
            PayTypes.WECHAT,
            'JSAPI',
            openid = tripartite.openid
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


class AddEvaluation(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc="订单物品id")
    request.evaluation_info = RequestField(
            DictField,
            desc="评价信息",
            conf={
                'tags': CharField(desc="评价标签:[tag1, tag2, ...]", is_required=False),
                'content': CharField(desc="评价内容", is_required=True),
                'pics': CharField(desc="图片链接:[pic1, pic2, ...]", is_required=False),
                'videos': CharField(desc="视频链接:[video1, video2, ...]", is_required=False),
                'server_attitude': IntField(desc="服务态度（1-5）", is_required=True),
                'course_quality': IntField(desc="课程质量（1-5）", is_required=True),
                'major': IntField(desc="院校专业（1-5）", is_required=True),
            }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加评论"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        order_item = OrderItemServer.get(request.order_item_id)
        if order_item.order.status != OrderStatus.ORDER_FINISHED:
            raise BusinessError("订单未完成， 不能评价。")
        if order_item.order.person_id != self.auth_user.person_id:
            raise BusinessError('非本人订单不能评价')
        request.evaluation_info.update({'order_item': order_item,
                                        'goods_id': order_item.goods_id,
                                        'person_id': order_item.order.person_id})
        OrderItemEvaluationServer.create(**request.evaluation_info)
        OrderItemServer.update(order_item, **{'evaluation': 'evaluated'})

    def fill(self, response):
        return response


class GetEvaluation(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc="订单物品id")

    response = with_metaclass(ResponseFieldSet)
    response.data = ResponseField(
        DictField,
        desc="评价信息",
        conf={
            'id': IntField(desc='评价id'),
            'content': CharField(desc="评价内容"),
            'tags': ListField(desc="评价标签列表",
                              fmt=CharField(desc="评价标签")),
            'pics': ListField(desc="评价图片列表",
                              fmt=CharField(desc="评价图片 ")),
            'videos': ListField(desc="评价视频列表",
                                fmt=CharField(desc="评价视频")),
            'hear_url': CharField(desc="用户头像"),
            'nickname': CharField(desc="用户昵称"),
            'create_time': DatetimeField(desc="创建时间")

        }

    )

    @classmethod
    def get_desc(cls):
        return "获取评价"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        search_info = {'order_item_id': request.order_item_id}
        order_evaluation = OrderItemEvaluationServer.get(request.current_page, **search_info)
        return order_evaluation

    def fill(self, response, order_evaluation):
        response.data = {
            'id': order_evaluation.id,
            'content': order_evaluation.content,
            'tags': json.loads(order_evaluation.tags),
            'pics': json.loads(order_evaluation.pics),
            'videos': json.loads(order_evaluation.videos),
            'hear_url': order_evaluation.hear_url,
            'nickname': order_evaluation.nick_name,
            'create_time': order_evaluation.create_time,
        }
        return response


class AllEvaluations(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc="订单物品id")

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="评价列表",
        fmt=DictField(
            desc="评价信息",
            conf={
                'id': IntField(desc='评价id'),
                'content': CharField(desc="评价内容"),
                'tags': ListField(desc="评价标签列表",
                                  fmt=CharField(desc="评价标签")),
                'pics': ListField(desc="评价图片列表",
                                  fmt=CharField(desc="评价图片 ")),
                'videos': ListField(desc="评价视频列表",
                                    fmt=CharField(desc="评价视频")),
                'hear_url': CharField(desc="用户头像"),
                'nickname': CharField(desc="用户昵称"),
                'create_time': DatetimeField(desc="创建时间")

            }
        )
    )
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "全部评价"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        search_info = {'goods_id': request.goods_id}
        splitor =OrderItemEvaluationServer.search(request.current_page, **search_info)
        return splitor

    def fill(self, response, splitor):
        response.data_list = [{
            'id': order_evaluation.id,
            'content': order_evaluation.content,
            'tags': json.loads(order_evaluation.tags),
            'pics': json.loads(order_evaluation.pics),
            'videos': json.loads(order_evaluation.videos),
            'hear_url': order_evaluation.hear_url,
            'nickname': order_evaluation.nick_name,
            'create_time': order_evaluation.create_time,
        } for order_evaluation in splitor.data]
        response.total = splitor.total
        response.total_page = splitor.total_page
        return response


class MyEvaluations(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页码")

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="评价列表",
        fmt=DictField(
            desc="订单信息",
            conf={
                'id': IntField(desc='评价id'),
                'content': CharField(desc="评价内容"),
                'tags': ListField(desc="评价标签列表",
                                  fmt=CharField(desc="评价标签")),
                'pics': ListField(desc="评价图片列表",
                                  fmt=CharField(desc="评价图片 ")),
                'videos': ListField(desc="评价视频列表",
                                    fmt=CharField(desc="评价视频")),
                'title': CharField(desc="商品标题"),
                'show_image': CharField(desc="商品图"),
                'school': CharField(desc="学校"),
                'major': CharField(desc="专业"),
                'create_time': DatetimeField(desc="创建时间")

            }
        )
    )
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "我的评价列表"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        # search_info = {}
        # if not self.auth_user.is_admin:
        search_info = {'person_id': self.auth_user.person_id}
        splitor = OrderItemEvaluationServer.search_my_evaluation(request.current_page, **search_info)
        return splitor

    def fill(self, response, splitor):
        response.data_list = [{
            'id': order_evaluation.id,
            'content': order_evaluation.content,
            'tags': json.loads(order_evaluation.tags),
            'pics': json.loads(order_evaluation.pics),
            'videos': json.loads(order_evaluation.videos),
            'title': order_evaluation.ms_obj.title,
            'show_image': order_evaluation.ms_obj.show_image,
            'school': order_evaluation.order_item.school_name,
            'major': order_evaluation.order_item.major_name,
            'create_time': order_evaluation.create_time,
        } for order_evaluation in splitor.data]
        response.total = splitor.total
        response.total_page = splitor.total_page
        return response
