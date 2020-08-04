# coding=UTF-8

'''
Created on 2016年7月23日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField,RequestFieldSet
from infrastructure.core.api.response import ResponseField,ResponseFieldSet
from infrastructure.core.field.base import CharField
from infrastructure.core.exception.business_error import BusinessError

from agile.base.api import NoAuthorizedApi
from abs.services.customer.account.manager import CustomerAccountServer
from abs.services.crm.tool.manager import SmsServer


class Phone(NoAuthorizedApi):

    request=with_metaclass(RequestFieldSet)
    request.number=RequestField(CharField,desc="手机号码")
    request.sms_type=RequestField(
        CharField,
        desc="短信类型",
        choices=(
            ('login', '登陆'),
            ('register','注册'),
            ('forget',"忘记密码"),
            ('bindcard',"绑定银行卡"),
        )
    )

    response=with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "获取手机验证码"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        check_result=CustomerAccountServer.is_exsited(request.number)
        if request.sms_type in ["register"] and check_result:
            raise BusinessError('此账号已存在')
        if request.sms_type in ["forget","bindcard"] and not check_result:
            raise BusinessError('此账号不存在')
        SmsServer.send_code(request.number,request.sms_type,"customer")

    def fill(self,response):
        return response


class Image(NoAuthorizedApi):

    request=with_metaclass(RequestFieldSet)

    response=with_metaclass(ResponseFieldSet)
    response.code=ResponseField(CharField,desc="图片验证码")

    @classmethod
    def get_desc(cls):
        return "获取登录图片验证码"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        return CustomerAccountServer.get_image_verification_code()

    def fill(self,response,code):
        response.code=code
        return response
