# coding=UTF-8

import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.agent.manager.api import AgentStaffAuthorizedApi
from infrastructure.core.exception.business_error import BusinessError
from abs.services.agent.order.utils.constant import PlanStatus
from abs.middleground.business.transaction.utils.constant import PayService
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.services.agent.order.manager import OrderServer, OrderPlanServer
from abs.services.agent.agent.manager import AgentStaffServer


class Add(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(
        IntField,
        desc = "订单id"
    )
    request.plan_info = RequestField(
        DictField,
        desc = "回款详情",
        conf = {
                'plan_amount': IntField(desc = "回款计划金额"),
                'plan_time': CharField(desc = "回款计划时间"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加回款计划"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        auth = self.auth_user
        order = OrderServer.get(request.order_id)
        if order.pay_services == PayService.FULL_PAYMENT:
            raise BusinessError('全款订单不允许添加回款计划')
        surplus_money = order.mg_order.strike_price - \
                        order.mg_order.payment.actual_amount
        OrderPlanServer.check_money(
            surplus_money,
            order,
            request.plan_info['plan_amount']
        )
        request.plan_info.update({"order":order, "staff_id":auth.id})
        OrderPlanServer.create(**request.plan_info)

    def fill(self, response):
        return response


class All(AgentStaffAuthorizedApi):
    """
    搜索订单回款计划
    """
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(
        IntField,
        desc = "订单id"
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "合同列表",
        fmt = DictField(
            desc = "合同详情",
            conf = {
                'id': IntField(desc = "回款计划id"),
                'plan_amount': CharField(desc = "回款计划金额"),
                'plan_time': CharField(desc = "回款计划时间"),
                'status':CharField(desc = "回款计划状态"),
                'status_name':CharField(desc = "回款计划状态"),
                'pay_type': CharField(desc = "付款方式"),
                'staff_name': CharField(desc = "回款计划人"),
                'create_time': DatetimeField(desc = "添加时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "订单回款计划查询接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        order = OrderServer.get(request.order_id)
        plan_qs = OrderPlanServer.search_all(order = order)
        AgentStaffServer.hung_staff(plan_qs)
        return plan_qs

    def fill(self, response, plan_qs):
        data_list = [{
            'id':plan.id,
            'plan_amount': plan.plan_amount,
            'plan_time': plan.plan_time,
            'status':plan.status,
            'status_name':plan.get_status_display(),
            'pay_type': '',
            'staff_name':plan.staff.name,
            'create_time': plan.create_time,
        } for plan in plan_qs]
        response.data_list = data_list
        return response


class Update(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.plan_id = RequestField(
        IntField,
        desc = "计划id"
    )
    request.plan_info = RequestField(
        DictField,
        desc = "回款详情",
        conf = {
                'plan_amount': IntField(desc = "回款计划金额"),
                'plan_time': CharField(desc = "回款计划时间"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "编辑回款计划接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        plan = OrderPlanServer.get(request.plan_id)
        if plan.status != PlanStatus.WAIT_PAY:
            raise BusinessError("此回款计划状态禁止编辑")
        order = OrderServer.get(plan.order.id)
        surplus_money = order.mg_order.strike_price - \
                        order.mg_order.payment.actual_amount
        OrderPlanServer.check_money(
            surplus_money,
            order,
            request.plan_info['plan_amount'],
            plan
        )
        OrderPlanServer.update(plan, **request.plan_info)

    def fill(self, response):
        return response


class Remove(AgentStaffAuthorizedApi):
    """删除回款计划"""
    request = with_metaclass(RequestFieldSet)
    request.plan_id = RequestField(IntField, desc = "计划id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "合同发送邮件接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        OrderPlanServer.remove(request.plan_id)

    def fill(self, response):
        return response


class paycode(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.plan_id = RequestField(IntField, desc = "计划id")

    response = with_metaclass(ResponseFieldSet)
    response.url = ResponseField(CharField, desc = "url")

    @classmethod
    def get_desc(cls):
        return "获取付款二维码"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        plan = OrderPlanServer.get(request.plan_id)
        order = OrderServer.get(plan.order.id)
        if plan.order.status in (OrderStatus.ORDER_LAUNCHED, OrderStatus.ORDER_CLOSED):
            raise BusinessError('此订单状态异常')
        if plan.status == PlanStatus.PAID:
            raise BusinessError('已回款订单无法查看二维码')
        surplus_money = order.mg_order.strike_price - \
                        order.mg_order.payment.actual_amount
        if plan.plan_amount > surplus_money:
            raise BusinessError("回款计划金额大于实际待付款金额,请删除后重新添加")
        url = OrderServer.paycode(plan, order)
        return url


    def fill(self, response, url):
        response.url = url
        return response
