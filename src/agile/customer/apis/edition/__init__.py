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
    request.type = RequestField(CharField, desc = "类型")

    response = with_metaclass(ResponseFieldSet)
    response.edition_info = ResponseField(
        DictField,
        desc = "版本信息",
        conf = {
            'number': CharField(desc = "版本号"),
            'url': CharField(desc = "版本更新连接"),
            'is_force_update': BooleanField(desc = "是否强制更新"),
            'content': CharField(desc = "更新描述")
        }
    )

    @classmethod
    def get_desc(cls):
        return "当前版本信息"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        return []

    def fill(self, response, edition):
        edition_info = {
            "number":"1.0",
            "url":"www.baidu.com",
            "is_force_update":True,
            "content":"请更新最新版本"
        }
        response.edition_info = edition_info
        return response
