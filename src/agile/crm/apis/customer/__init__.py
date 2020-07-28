# coding=UTF-8

from infrastructure.core.field.base import CharField,DictField,\
        IntField,ListField,DatetimeField,BooleanField, MobileCheckField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField,RequestFieldSet
from infrastructure.core.api.response import ResponseField,ResponseFieldSet

from agile.crm.manager.api import StaffAuthorizedApi
from abs.middleground.business.transaction.manager import TransactionServer
from abs.services.customer.personal.manager import CustomerServer
from abs.services.customer.account.manager import CustomerAccountServer
from abs.services.customer.finance.manager import CustomerFinanceServer


class Add(StaffAuthorizedApi):
    request=with_metaclass(RequestFieldSet)
    request.customer_info=RequestField(
        DictField,
        desc="客户详情",
        conf={
            'nick': CharField(desc="昵称",is_required=False),
            'head_url': CharField(desc="头像",is_required=False),
            'name': CharField(desc="姓名",is_required=False),
            'gender': CharField(desc="性别",is_required=False),
            'birthday': CharField(desc="生日",is_required=False),
            'phone': MobileCheckField(desc="手机号"),
            'email': CharField(desc="邮箱",is_required=False),
            'wechat': CharField(desc="微信",is_required=False),
            'qq': CharField(desc="qq",is_required=False),
        }
    )

    response=with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加客户接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        print(request.customer_info)

    def fill(self,response):
        return response


class Search(StaffAuthorizedApi):
    request=with_metaclass(RequestFieldSet)
    request.current_page=RequestField(IntField,desc="当前页码")
    request.search_info=RequestField(DictField,desc="搜索客户条件",conf={
        'nick': CharField(desc="昵称",is_required=False),
        'create_time__gte': DatetimeField(desc="注册起始时间",is_required=False),
        'create_time__lte': DatetimeField(desc="注册结束时间",is_required=False),
    })

    response=with_metaclass(ResponseFieldSet)
    response.total=ResponseField(IntField,desc="数据总数")
    response.total_page=ResponseField(IntField,desc="总页码数")
    response.data_list=ResponseField(
        ListField,
        desc="用户列表",
        fmt=DictField(
            desc="用户详情",
            conf={
                'id': IntField(desc="客户编号"),
                'nick': CharField(desc="昵称"),
                'head_url': CharField(desc="头像"),
                'name': CharField(desc="姓名"),
                'gender': CharField(desc="性别"),
                'birthday': CharField(desc="生日"),
                'phone': CharField(desc="手机号"),
                'email': CharField(desc="邮箱"),
                'wechat': CharField(desc="微信"),
                'qq': CharField(desc="qq"),
                'username': CharField(desc="账号"),
                'status': CharField(desc="账号状态"),
                'create_time': DatetimeField(desc="注册时间"),
            }
        )
    )


    @classmethod
    def get_desc(cls):
        return "搜索客户"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        customer_spliter=CustomerServer.search(
            request.current_page,
            **request.search_info
        )
        customer_spliter.data=CustomerAccountServer.hung_account(
            customer_spliter.data
        )
        return customer_spliter

    def fill(self,response,customer_spliter):
        data_list=[{
            'id': customer.id,
            'nick': customer.nick,
            'head_url': customer.head_url,
            'name': customer.person.name,
            'gender': customer.person.gender,
            'birthday': customer.person.birthday,
            'phone': customer.person.phone,
            'email': customer.person.email,
            'wechat': customer.person.wechat,
            'qq': customer.person.qq,
            'username': customer.account.username,
            'status':customer.account.status,
            'create_time': customer.create_time
        } for customer in customer_spliter.data]
        response.data_list=data_list
        response.total=customer_spliter.total
        response.total_page=customer_spliter.total_page
        return response


class Get(StaffAuthorizedApi):
    """获取客户详情接口"""
    request=with_metaclass(RequestFieldSet)
    request.customer_id=RequestField(IntField,desc="客户id")

    response=with_metaclass(ResponseFieldSet)
    response.customer_info=ResponseField(
        DictField,
        desc="用户详情",
        conf={
            'id': IntField(desc="客户编号"),
            'nick': CharField(desc="昵称"),
            'head_url': CharField(desc="头像"),
            'name': CharField(desc="姓名"),
            'gender': CharField(desc="性别"),
            'birthday': CharField(desc="生日"),
            'phone': CharField(desc="手机号"),
            'email': CharField(desc="邮箱"),
            'wechat': CharField(desc="微信"),
            'qq': CharField(desc="qq"),
            'create_time': DatetimeField(desc="注册时间"),
            'username': CharField(desc="账号"),
            'status': CharField(desc="账号状态"),
            'is_realname': BooleanField(desc="是否实名"),
            'balance': IntField(desc="余额"),
            'realname_info':DictField(desc='实名详情',conf={
                'name': CharField(desc="姓名"),
                'identification': CharField(desc="身份证号"),
                'id_front': CharField(desc="身份证正面"),
                'id_back': CharField(desc="身份证反面"),
                'id_in_band': CharField(desc="手持身份证"),
                'remark': CharField(desc="备注"),
             }),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取客户详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        customer=CustomerServer.get(request.customer_id)
        CustomerAccountServer.hung_account([customer])
        customer.balance=TransactionServer.get_person_balance(
             customer.person_id
        )
        return customer

    def fill(self,response,customer):
        is_realname=True if customer.person_status.certification else False
        response.customer_info={
            'id': customer.id,
            'nick': customer.nick,
            'head_url': customer.head_url,
            'name': customer.person.name,
            'gender': customer.person.gender,
            'birthday': customer.person.birthday,
            'phone': customer.person.phone,
            'email': customer.person.email,
            'wechat': customer.person.wechat,
            'qq': customer.person.qq,
            'create_time': customer.create_time,
            'username': customer.account.username,
            'status':customer.account.status,
            'is_realname':is_realname,
            'balance':customer.balance,
            'realname_info':{
                'name': customer.person_status.certification.name if is_realname else "",
                'identification': customer.person_status.certification.identification if is_realname else "",
                'id_front':customer.person_status.certification.id_front if is_realname else "",
                'id_back': customer.person_status.certification.id_back if is_realname else "",
                'id_in_band':customer.person_status.certification.id_in_hand if is_realname else "",
                'remark':customer.person_status.certification.remark if is_realname else "",
             },
        }
        return response


class Update(StaffAuthorizedApi):
    """修改客户信息"""
    request=with_metaclass(RequestFieldSet)
    request.customer_id=RequestField(IntField,desc="客户id")
    request.customer_info=RequestField(
        DictField,
        desc="客户修改详情",
        conf={
            'nick': CharField(desc="昵称",is_required=False),
            'head_url': CharField(desc="头像",is_required=False),
            'name': CharField(desc="姓名",is_required=False),
            'gender': CharField(desc="性别",is_required=False),
            'birthday': CharField(desc="生日",is_required=False),
            'phone': MobileCheckField(desc="电话",is_required=False),
            'email': CharField(desc="邮箱",is_required=False),
            'wechat': CharField(desc="微信",is_required=False),
            'qq': CharField(desc="qq",is_required=False),
        }
    )

    response=with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户个人中心修改接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        CustomerServer.update(
            request.customer_id,
            **request.customer_info
        )

    def fill(self,response):
        return response
