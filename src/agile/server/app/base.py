# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService
from abs.middleware.rule import rule_register, permise_rules, staff_rules, \
    communication_rules, eventonlineservice_rules, wechatmanage_rules

# from agile.apis import test


class CrmService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "用户服务"

    @classmethod
    def get_desc(self):
        return "针对注册登录用户提供服务"

    @classmethod
    def get_flag(cls):
        return "crm"


crm_service = CrmService()
from agile.apis.staff import Add, Get, Update, Search 
crm_service.add(Add, Get, Update, Search)

from agile.apis.staff.myself import Get, Update
crm_service.add(Get, Update)

# from agile.apis.staff.token import Renew
# crm_service.add(Renew)

from agile.apis.staff.account import Login, Logout
crm_service.add(Login, Logout)
from agile.apis.staff.account.vcode import Phone, Image
crm_service.add(Phone, Image)
