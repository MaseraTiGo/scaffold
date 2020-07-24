# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService


class MiddlegroundService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "中台服务"

    @classmethod
    def get_desc(self):
        return "中台传输服务"

    @classmethod
    def get_flag(cls):
        return "middleground"


middleground_service = MiddlegroundService()
from agile.middleground.apis.merchandise import Add, Search, Get, Update, Remove
middleground_service.add(Add, Search, Get, Update, Remove)

from agile.middleground.apis.merchandise.specification import Add, Get, Update, Remove
middleground_service.add(Add, Get, Update, Remove)
