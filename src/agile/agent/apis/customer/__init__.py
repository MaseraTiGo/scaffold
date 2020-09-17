# coding=UTF-8
import json
import copy
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.event.utils.constant import OperationTypes
from abs.services.agent.customer.manager import AgentCustomerServer
from abs.services.agent.event.manager import OperationEventServer


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
            'name': agent_customer.name,
            'gender': agent_customer.person.gender if \
                      agent_customer.person else '',
            'birthday': agent_customer.person.birthday if \
                        agent_customer.person else '',
            'phone': agent_customer.phone,
            'email': agent_customer.person.email if \
                     agent_customer.person else '',
            'wechat': agent_customer.person.wechat if \
                      agent_customer.person else '',
            'qq': agent_customer.person.qq if \
                  agent_customer.person else '',
            'create_time': agent_customer.create_time
        } for agent_customer in agent_customer_spliter.data]
        response.data_list = data_list
        response.total = agent_customer_spliter.total
        response.total_page = agent_customer_spliter.total_page
        return response


class Update(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.agent_customer_id = RequestField(IntField, desc = "代理商客户id")
    request.update_info = RequestField(
        DictField,
        desc = "需要更新的客户信息",
        conf = {
            'name': CharField(desc = "客户姓名", is_required = False),
            'phone': CharField(desc = "客户电话", is_required = False),
            'gender': CharField(desc = "客户性别", is_required = False),
            'city': CharField(desc = "省市区", is_required = False),
            'source': CharField(desc = "客户来源", is_required = False),
            'wechat': CharField(desc = "微信", is_required = False),
            'qq': CharField(desc = "QQ号码", is_required = False),
            'education': CharField(desc = "学历", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "完善客户接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent_customer = AgentCustomerServer.get(request.agent_customer_id)
        o_agent_customer = copy.copy(agent_customer)
        agent_customer = AgentCustomerServer.update(
            agent_customer,
            **request.update_info
        )
        if len(request.update_info) > 0:
            describe = ""
            mapping = {"name":"客户姓名", "phone":"客户电话", \
                     "gender":"客户性别", "city":"客户地址", \
                     "source":"客户来源", "wechat":"客户微信", \
                     "qq":"客户QQ", "education":"客户学历"}

            for k, v in request.update_info.items():
                if getattr(o_agent_customer, k) != getattr(agent_customer, k):
                   describe = "{d}{v}由{o}变更为{n};".format(
                        d = describe,
                        v = mapping[k],
                        o = getattr(o_agent_customer, k),
                        n = getattr(agent_customer, k)
                    )
            if describe:
                auth = self.auth_user
                OperationEventServer.create(**{
                    "staff_id":auth.id,
                    "organization_id":0,
                    "agent_customer_id":agent_customer.id,
                    "agent_id":auth.agent_id,
                    "type":OperationTypes.CUSTOMER,
                    "describe":describe
                })



    def fill(self, response, address_list):
        return response
