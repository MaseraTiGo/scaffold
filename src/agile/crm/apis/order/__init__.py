# coding=UTF-8

import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.customer.order.utils.constant import OrderSource
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.services.customer.order.manager import OrderServer, OrderItemServer
from abs.middleground.business.transaction.utils.constant import \
        PayTypes, OwnTypes
from abs.middleground.business.merchandise.utils.constant import \
        DespatchService
from abs.services.agent.goods.utils.constant import DurationTypes
from abs.services.customer.personal.manager import CustomerServer
from abs.services.crm.agent.manager import AgentServer


class Get(StaffAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc = "订单id")

    response = with_metaclass(ResponseFieldSet)
    response.order_info = ResponseField(
        DictField,
        desc = "订单详情",
        conf = {
            'id': IntField(desc = "订单id"),
            'nick': CharField(desc = "客户姓名"),
            'phone': CharField(desc = "客户手机号"),
            'register_time': DatetimeField(desc = "客户注册时间"),

            're_name': CharField(desc = "收货人姓名"),
            're_phone': CharField(desc = "收货人手机号"),
            're_address': CharField(desc = "收货人地址"),

            'mg_order_id':IntField(desc = "中台订单id"),
            'number': CharField(desc = "订单编号"),
            'strike_price': IntField(desc = "成交金额，单位：分"),
            'actual_amount': CharField(desc = "实付金额,单位：分"),
            'source':CharField(
                            desc = "订单来源类型",
                            choices = OrderSource.CHOICES
                        ),
            'description': CharField(desc = "订单描述"),
            'status': CharField(
                desc = "订单状态",
                choices = OrderStatus.CHOICES
            ),
            'remark': CharField(desc = "订单备注"),
            'create_time': DatetimeField(desc = "订单创建时间"),

            'snapshoot_list': ListField(
                desc = '商品列表',
                fmt = DictField(
                    desc = "商品详情",
                    conf = {
                        'id': CharField(desc = "商品快照id"),
                        'show_image': CharField(desc = "商品图片"),
                        'title': CharField(desc = "商品标题"),
                        'brand_name': CharField(desc = "品牌名称"),
                        'production_name': CharField(desc = "产品名称"),
                        'count': IntField(desc = "商品数量"),
                        'school_name': CharField(desc = "学校名称"),
                        'major_name': CharField(desc = "专业名称"),
                        'sale_price': IntField(desc = "商品单价"),
                        'duration':CharField(
                            desc = "学制",
                            choices = DurationTypes.CHOICES
                        ),
                        'total_price': IntField(desc = "总价"),
                        'remark': CharField(desc = "属性"),
                    }
                )
            ),


        }
    )
    @classmethod
    def get_desc(cls):
        return "订单信息查询接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        order = OrderServer.get(request.order_id)
        customer = CustomerServer.get(order.customer_id)
        OrderItemServer.hung_order_item([order])
        return order, customer

    def fill(self, response, order, customer):
        response.order_info = {
            'id': order.id,
            'nick':customer.nick,
            'phone':customer.person.phone,

            'register_time':customer.create_time,

            're_name':order.mg_order.invoice.name if \
                      order.mg_order.invoice else "",
            're_phone':order.mg_order.invoice.phone if \
                      order.mg_order.invoice else "",
            're_address':order.mg_order.invoice.address if \
                      order.mg_order.invoice else "",

            'mg_order_id':order.mg_order.id,
            'number': order.mg_order.number,
            'strike_price': order.mg_order.strike_price,
            'actual_amount': order.mg_order.payment.actual_amount if \
                             order.mg_order.payment else 0,
            'source': order.source,
            'description': order.mg_order.description,
            'remark': order.mg_order.remark,
            'status': order.mg_order.status,
            'create_time': order.mg_order.create_time,

            'snapshoot_list': [
                {
                    'id': orderitem.id,
                    'show_image':orderitem.snapshoot.show_image,
                    'title': orderitem.snapshoot.title,
                    'brand_name':orderitem.snapshoot.brand_name,
                    'production_name':orderitem.snapshoot.production_name,
                    'count': orderitem.snapshoot.count,
                    'school_name':orderitem.school_name,
                    'major_name':orderitem.major_name,
                    'sale_price': orderitem.snapshoot.count,
                    'duration':orderitem.duration,
                    'total_price': orderitem.snapshoot.total_price,
                    'remark': orderitem.snapshoot.remark,
                }
                for orderitem in order.orderitem_list
            ],
        }
        return response


class Search(StaffAuthorizedApi):
    """
    搜索订单
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc = "当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc = "搜索订单条件",
        conf = {
          'number': CharField(desc = "订单号", is_required = False),
          'agent_id': IntField(desc = "代理商id", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "订单列表",
        fmt = DictField(
            desc = "订单详情",
            conf = {
                'id': IntField(desc = "订单id"),
                'number': CharField(desc = "订单编号"),
                'last_payment_time': DatetimeField(desc = "最后支付时间"),
                'source':CharField(
                            desc = "订单来源类型",
                            choices = OrderSource.CHOICES
                        ),
                'create_time': DatetimeField(desc = "订单创建时间"),

                'strike_price': IntField(desc = "成交金额，单位：分"),
                'actual_amount': CharField(desc = "实付金额,单位：分"),
                'status': CharField(
                    desc = "订单状态",
                    choices = OrderStatus.CHOICES
                ),

                'nick': CharField(desc = "客户昵称"),
                'phone': CharField(desc = "客户手机号"),
                'agent_id': IntField(desc = "代理商id"),
                'agent_name': CharField(desc = "公司名称"),
                'snapshoot_list': ListField(
                    desc = '商品列表',
                    fmt = DictField(
                        desc = "商品详情",
                        conf = {
                            'id': CharField(desc = "商品快照id"),
                            'show_image': CharField(desc = "商品图片"),
                            'title': CharField(desc = "商品标题"),
                            'brand_name': CharField(desc = "品牌名称"),
                            'production_name': CharField(desc = "产品名称"),
                            'count': IntField(desc = "商品数量"),
                            'school_name': CharField(desc = "学校名称"),
                            'major_name': CharField(desc = "专业名称"),
                            'sale_price': IntField(desc = "商品单价"),
                            'duration':CharField(
                                desc = "学制",
                                choices = DurationTypes.CHOICES
                            ),
                            'total_price': IntField(desc = "总价"),
                            'remark': CharField(desc = "属性"),
                        }
                    )
                ),
            }
        )
    )
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "订单搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        order_spliter = OrderServer.search(
            request.current_page,
            **request.search_info
        )
        OrderItemServer.hung_order_item(order_spliter.get_list())
        CustomerServer.hung_customer(order_spliter.get_list())
        AgentServer.hung_agent(order_spliter.get_list())
        return order_spliter

    def fill(self, response, order_spliter):
        data_list = [{
            'id': order.id,
            'number': order.mg_order.number,
            'last_payment_time': order.mg_order.payment.last_payment_time if \
                                 order.mg_order.payment else None,
            'source': order.source,
            'create_time': order.create_time,

            'strike_price': order.mg_order.strike_price,
            'actual_amount': order.mg_order.payment.actual_amount if \
                             order.mg_order.payment else 0,
            'status': order.mg_order.status,

            'nick':  order.customer.nick,
            'phone': order.customer.person.phone,
            'agent_id': order.agent.id,
            'agent_name': order.agent.name,
            'snapshoot_list': [
                {
                    'id': orderitem.id,
                    'show_image':orderitem.snapshoot.show_image,
                    'title': orderitem.snapshoot.title,
                    'brand_name':orderitem.snapshoot.brand_name,
                    'production_name':orderitem.snapshoot.production_name,
                    'count': orderitem.snapshoot.count,
                    'school_name':orderitem.school_name,
                    'major_name':orderitem.major_name,
                    'sale_price': orderitem.snapshoot.count,
                    'duration':orderitem.duration,
                    'total_price': orderitem.snapshoot.total_price,
                    'remark': orderitem.snapshoot.remark,
                }
                for orderitem in order.orderitem_list
            ],

        } for order in order_spliter.data]
        response.data_list = data_list
        response.total = order_spliter.total
        response.total_page = order_spliter.total_page
        return response
