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
from agile.middleground.apis.business.merchandise import Add, Search, Get, Update, Remove
middleground_service.add(Add, Search, Get, Update, Remove)

from agile.middleground.apis.business.merchandise.specification import Add, Get, Update, Remove
middleground_service.add(Add, Get, Update, Remove)

from agile.middleground.apis.business.order import Place, Pay, PayCallback, Delivery, Finish, Close, Get, Search
middleground_service.add(Place, Pay, PayCallback, Delivery, Finish, Close, Get, Search)

from agile.middleground.apis.technology.permission import Get
middleground_service.add(Get)

from agile.middleground.apis.technology.permission.platform import Authorize, Apply, Forbidden, Refresh
middleground_service.add(Authorize, Apply, Forbidden, Refresh)

from agile.middleground.apis.technology.permission.rule import Add, All, Get, Update, Remove
middleground_service.add(Add, All, Get, Update, Remove)

from agile.middleground.apis.technology.permission.organization import Add, All, Get, Update, Remove
middleground_service.add(Add, All, Get, Update, Remove)

from agile.middleground.apis.technology.permission.rulegroup import Add, Search, Get, Update, Remove
middleground_service.add(Add, Search, Get, Update, Remove)

from agile.middleground.apis.technology.permission.position import Add, All, Get, Update, Remove
middleground_service.add(Add, All, Get, Update, Remove)

from agile.middleground.apis.technology.permission.bind import Position, Person
middleground_service.add(Position, Person)
