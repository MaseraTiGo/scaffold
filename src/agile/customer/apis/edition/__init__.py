# coding=UTF-8
import json
import datetime
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from infrastructure.core.exception.business_error import BusinessError


class Get(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.edition_info = ResponseField(DictField, desc = "版本信息", conf = {
        'number': CharField(desc = "版本号"),
        'is_force_update': BooleanField(desc = "是否强制更新"),
        'url': CharField(desc = "更新连接")
    })

    @classmethod
    def get_desc(cls):
        return "当前版本信息"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        return None

    def fill(self, response):
        response.edition_info = {
            "number":"2.0",
            "is_force_update":True,
            "url":"www.baidu.com"
        }
        return response
