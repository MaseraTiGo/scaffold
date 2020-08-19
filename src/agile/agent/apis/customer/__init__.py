# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.agent.manager.api import AgentStaffAuthorizedApi

from abs.services.agent.customer.manager import AgentCustomerServer


class Search(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页码")
    request.search_info = RequestField(DictField, desc = "搜索客户条件", conf = {
        'name': CharField(desc = "姓名", is_required = False),
        'phone': CharField(desc = "手机号码", is_required = False),
        'create_time__gte': DatetimeField(
            desc = "注册起始时间",
            is_required = False
        ),
        'create_time__lte': DatetimeField(
            desc = "注册结束时间",
            is_required = False
        ),
    })

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "用户列表",
        fmt = DictField(
            desc = "用户详情",
            conf = {
                'id': IntField(desc = "客户编号"),
                'nick': CharField(desc = "昵称"),
                'head_url': CharField(desc = "头像"),
                'name': CharField(desc = "姓名"),
                'gender': CharField(desc = "性别"),
                'birthday': CharField(desc = "生日"),
                'phone': CharField(desc = "手机号"),
                'email': CharField(desc = "邮箱"),
                'wechat': CharField(desc = "微信"),
                'qq': CharField(desc = "qq"),
                'create_time': DatetimeField(desc = "注册时间"),
            }
        )
    )


    @classmethod
    def get_desc(cls):
        return "搜索客户"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        auth = self.auth_user
        request.search_info.update({
            "agent_id":auth.agent_id
        })
        agent_customer_spliter = AgentCustomerServer.search(
            request.current_page,
            **request.search_info
        )
        return agent_customer_spliter

    def fill(self, response, agent_customer_spliter):
        data_list = [{
            'id': agent_customer.id,
            'nick': agent_customer.customer.nick if \
                    agent_customer.customer else '',
            'head_url': agent_customer.customer.head_url if \
                        agent_customer.customer else '',
            'name': agent_customer.customer.person.name if \
                    agent_customer.customer else '',
            'gender': agent_customer.customer.person.gender if \
                      agent_customer.customer else '',
            'birthday': agent_customer.customer.person.birthday if \
                        agent_customer.customer else '',
            'phone': agent_customer.phone,
            'email': agent_customer.customer.person.email if \
                     agent_customer.customer else '',
            'wechat': agent_customer.customer.person.wechat if \
                      agent_customer.customer else '',
            'qq': agent_customer.customer.person.qq if \
                  agent_customer.customer else '',
            'create_time': agent_customer.create_time
        } for agent_customer in agent_customer_spliter.data]
        response.data_list = data_list
        response.total = agent_customer_spliter.total
        response.total_page = agent_customer_spliter.total_page
        return response
