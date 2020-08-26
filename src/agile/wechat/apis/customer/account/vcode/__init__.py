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
from abs.services.crm.tool.manager import SmsServer


class Phone(NoAuthorizedApi):
    request=with_metaclass(RequestFieldSet)
    request.number=RequestField(CharField,desc="手机号码")
    request.sms_type=RequestField(
        CharField,
        desc="短信类型",
        choices=(
            ('wechat_register', '注册'),
        )
    )

    response=with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "获取手机验证码"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        SmsServer.send_code(
            request.number,
            request.sms_type,
            "customer_wechat"
        )

    def fill(self, response):
        return response# coding=UTF-8

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
from abs.services.crm.tool.manager import SmsServer


class Phone(NoAuthorizedApi):
    request=with_metaclass(RequestFieldSet)
    request.number=RequestField(CharField,desc="手机号码")
    request.sms_type=RequestField(
        CharField,
        desc="短信类型",
        choices=(
            ('wechat_register', '注册'),
        )
    )

    response=with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "获取手机验证码"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        SmsServer.send_code(
            request.number,
            request.sms_type,
            "customer_wechat"
        )

    def fill(self, response):
        return response