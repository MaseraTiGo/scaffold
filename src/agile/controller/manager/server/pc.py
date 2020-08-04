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
from agile.controller.apis.staff import Add, Get, Update, Search
controller_pc_service.add(Add, Get, Update, Search)

from agile.controller.apis.staff.myself import Get, Update
controller_pc_service.add(Get, Update)

# from agile.controller.apis.staff.token import Renew
# controller_pc_service.add(Renew)

from agile.controller.apis.staff.account import Login, Logout
controller_pc_service.add(Login, Logout)

from agile.controller.apis.staff.account.vcode import Phone, Image
controller_pc_service.add(Phone, Image)

from agile.controller.apis.staff.account.password import Modify
controller_pc_service.add(Modify)
