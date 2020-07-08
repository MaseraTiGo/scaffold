# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.service.customer.manager import CustomerServer


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.customer_info = RequestField(DictField, desc = "客户详情", conf = {
        'name': CharField(desc = "姓名", is_required = False),
        'gender': CharField(desc = "性别", is_required = False),
        'birthday': CharField(desc = "生日", is_required = False),
        'phone': CharField(desc = "手机号"),
        'email': CharField(desc = "邮箱", is_required = False),
        'wechat': CharField(desc = "微信", is_required = False),
        'qq': CharField(desc = "qq", is_required = False),
        'education': CharField(desc = "学历", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加客户接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        print(request.customer_info)

    def fill(self, response):
        return response



class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页码")
    request.search_info = RequestField(DictField, desc = "搜索客户条件", conf = {
        'name': CharField(desc = "姓名", is_required = False),
        'phone': CharField(desc = "手机", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(ListField, desc = "用户列表", fmt = \
                                       DictField(desc = "用户详情", conf = {
                                            'id': IntField(desc = "客户编号"),
                                            'name': CharField(desc = "姓名"),
                                            'gender': CharField(desc = "性别"),
                                            'birthday': CharField(desc = "生日"),
                                            'phone': CharField(desc = "手机号"),
                                            'email': CharField(desc = "邮箱"),
                                            'wechat': CharField(desc = "微信"),
                                            'qq': CharField(desc = "qq"),
                                            'education': CharField(desc = "学历"),
                                            }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")


    @classmethod
    def get_desc(cls):
        return "搜索客户"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        customer_spliter = CustomerServer.search(request.current_page, **request.search_info)
        return customer_spliter

    def fill(self, response, customer_spliter):
        data_list = [{
            'id': customer.id,
            'name': customer.name,
            'gender': customer.gender,
            'birthday': customer.birthday,
            'phone': customer.phone,
            'email': customer.email,
            'education': customer.education,
            'wechat': customer.wechat,
            'qq': customer.qq,
        } for customer in customer_spliter.data]
        response.data_list = data_list
        response.total = customer_spliter.total
        response.total_page = customer_spliter.total_page
        return response


class Get(StaffAuthorizedApi):
    """获取客户详情接口"""
    request = with_metaclass(RequestFieldSet)
    request.customer_id = RequestField(IntField, desc = "客户id")

    response = with_metaclass(ResponseFieldSet)
    response.customer_info = ResponseField(DictField, desc = "用户详情", conf = {
            'id': IntField(desc = "客户编号"),
            'name': CharField(desc = "姓名"),
            'gender': CharField(desc = "性别"),
            'birthday': CharField(desc = "生日"),
            'phone': CharField(desc = "手机号"),
            'email': CharField(desc = "邮箱"),
            'wechat': CharField(desc = "微信"),
            'qq': CharField(desc = "qq"),
            'education': CharField(desc = "学历"),
    })

    @classmethod
    def get_desc(cls):
        return "获取客户详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return CustomerServer.get_byid(request.customer_id)

    def fill(self, response, customer):
        response.customer_info = {
            'id': customer.id,
            'name': customer.name,
            'gender': customer.gender,
            'birthday': customer.birthday,
            'phone': customer.phone,
            'email': customer.email,
            'education': customer.education,
            'wechat': customer.wechat,
            'qq': customer.qq,
        }
        return response



class Update(StaffAuthorizedApi):
    """修改客户信息"""
    request = with_metaclass(RequestFieldSet)
    request.customer_id = RequestField(IntField, desc = "客户id")
    request.customer_info = RequestField(DictField, desc = "客户修改详情", conf = {
        'name': CharField(desc = "姓名", is_required = False),
        'gender': CharField(desc = "性别", is_required = False),
        'birthday': CharField(desc = "生日", is_required = False),
        'phone': CharField(desc = "电话", is_required = False),
        'email': CharField(desc = "邮箱", is_required = False),
        'wechat': CharField(desc = "微信", is_required = False),
        'qq': CharField(desc = "qq", is_required = False),
        'education': CharField(desc = "学历", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户个人中心修改接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        CustomerServer.update(request.customer_id, **request.customer_info)

    def fill(self, response):
        return response
