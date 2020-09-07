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
from abs.services.agent.order.manager import OrderServer, OrderPlanServer
from abs.services.agent.staff.manager import AgentStaffServer


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
    request.url = ResponseField(CharField, desc = "url")

    @classmethod
    def get_desc(cls):
        return "获取付款二维码"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        pass

    def fill(self, response):
        response.url = "www.baidu.com"
        return response
