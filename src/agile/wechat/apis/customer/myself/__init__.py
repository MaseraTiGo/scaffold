# coding=UTF-8

'''
Created on 2020年6月18日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField, BooleanField, MobileField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.wechat.manager.api import WechatAuthorizedApi
from abs.services.customer.personal.manager import CustomerServer
from abs.middleground.business.person.manager import PersonServer


class Get(WechatAuthorizedApi):
    """
    获取个人中心详情
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.customer_info = ResponseField(DictField, desc="用户详情", conf={
        'nick': CharField(desc="昵称"),
        'head_url': CharField(desc="头像"),
        'name': CharField(desc="姓名"),
        'gender': CharField(desc="性别"),
        'birthday': CharField(desc="生日"),
        'phone': CharField(desc="手机号"),
        'email': CharField(desc="邮箱"),
        'wechat': CharField(desc="微信"),
        'qq': CharField(desc="qq"),
        'is_certify': BooleanField(desc="是否认证")
    })

    @classmethod
    def get_desc(cls):
        return "客户个人中心详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        customer = CustomerServer.get(self.auth_user.id)
        customer.person_status = PersonServer.get_person_status(customer.person_id)
        return customer

    def fill(self, response, customer):
        response.customer_info = {
            'nick': customer.nick,
            'head_url': customer.head_url,
            'name': customer.person.name,
            'gender': customer.person.gender,
            'birthday': customer.person.birthday,
            'phone': customer.person.phone,
            'email': customer.person.email,
            'wechat': customer.person.wechat,
            'qq': customer.person.qq,
            'is_certify': True if customer.person_status.certification else False
        }
        return response


class Update(WechatAuthorizedApi):
    """
    修改个人中心详情
    """
    request = with_metaclass(RequestFieldSet)
    request.myself_info = RequestField(DictField, desc="客户修改详情", conf={
        'nick': CharField(desc="昵称", is_required=False),
        'head_url': CharField(desc="头像", is_required=False),
        'name': CharField(desc="姓名", is_required=False),
        'gender': CharField(desc="性别", is_required=False),
        'birthday': CharField(desc="生日", is_required=False),
        'phone': MobileField(desc="电话", is_required=False),
        'email': CharField(desc="邮箱", is_required=False),
        'wechat': CharField(desc="微信", is_required=False),
        'qq': CharField(desc="qq", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户个人中心修改接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        customer = self.auth_user
        CustomerServer.update(customer.id, **request.myself_info)

    def fill(self, response):
        return response
