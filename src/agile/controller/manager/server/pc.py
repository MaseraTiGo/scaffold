# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService


class ControllerPcService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "中台控制服务"

    @classmethod
    def get_desc(self):
        return "针对中台进行相关的管理服务"

    @classmethod
    def get_flag(cls):
        return "controller-pc"


controller_pc_service = ControllerPcService()
from agile.controller.apis.enterprise import Search
controller_pc_service.add(Search)

from agile.controller.apis.staff import Add, Get, Update, Search
controller_pc_service.add(Add, Get, Update, Search)

from agile.controller.apis.staff.myself import Get, Update
controller_pc_service.add(Get, Update)

# from agile.controller.apis.staff.token import Renew
# controller_pc_service.add(Renew)

from agile.controller.apis.staff.account import Login, Logout, Get, Update
controller_pc_service.add(Login, Logout, Get, Update)

from agile.controller.apis.staff.account.vcode import Phone, Image
controller_pc_service.add(Phone, Image)

from agile.controller.apis.staff.account.password import Modify
controller_pc_service.add(Modify)

from agile.controller.apis.staff.permission import Get
controller_pc_service.add(Get)

from agile.controller.apis.staff.permission.platform import Add, Get, Remove, Search, Update
controller_pc_service.add(Add, Get, Search, Update, Remove)

from agile.controller.apis.staff.permission.authorization import Get, Remove, Search, Update, Authorize, Apply, Forbidden, Refresh
controller_pc_service.add(Get, Search, Update, Remove, Authorize, Apply, Forbidden, Refresh)

from agile.controller.apis.staff.permission.rule import Add, All, Get, Update, Remove
controller_pc_service.add(Add, All, Get, Update, Remove)

from agile.controller.apis.staff.permission.organization import Add, All, Search, Get, Update, Remove
controller_pc_service.add(Add, All, Search, Get, Update, Remove)

from agile.controller.apis.staff.permission.rulegroup import Add, Search, Get, Update, Remove
controller_pc_service.add(Add, Search, Get, Update, Remove)

from agile.controller.apis.staff.permission.position import Add, All, Search, Get, Update, Remove
controller_pc_service.add(Add, All, Search, Get, Update, Remove)

from agile.controller.apis.staff.permission.bind import Position, Person
controller_pc_service.add(Position, Person)
