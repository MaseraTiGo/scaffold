# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.services.agent.order.manager import OrderServer
from abs.services.customer.personal.manager import CustomerServer


class Search(StaffAuthorizedApi):
    """
    搜索订单
    """
    request = with_metaclass(RequestFieldSet)
    request.customer_id = RequestField(IntField, desc = "客户id")
    request.current_page = RequestField(
        IntField,
        desc = "当前页码"
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
                'create_time': DatetimeField(desc = "订单创建时间"),
                'actual_amount': CharField(desc = "实付金额,单位：分"),
                'status': CharField(
                    desc = "订单状态",
                    choices = OrderStatus.CHOICES
                ),
            }
        )
    )
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "客户订单搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        customer = CustomerServer.get(
            request.customer_id
        )
        search_info = {
            "person_id":customer.person_id,
        }
        order_spliter = OrderServer.search(
            request.current_page,
            **search_info
        )
        return order_spliter

    def fill(self, response, order_spliter):
        data_list = [{
            'id': order.id,
            'number': order.mg_order.number,
            'last_payment_time': order.mg_order.payment.last_payment_time if \
                                 order.mg_order.payment else None,
            'create_time': order.create_time,
            'actual_amount': order.mg_order.payment.actual_amount if \
                             order.mg_order.payment else 0,
            'status': order.mg_order.status,
        } for order in order_spliter.data]
        response.data_list = data_list
        response.total = order_spliter.total
        response.total_page = order_spliter.total_page
        return response
