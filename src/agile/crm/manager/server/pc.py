# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService


class CrmPcService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "用户服务"

    @classmethod
    def get_desc(self):
        return "针对注册登录用户提供服务"

    @classmethod
    def get_flag(cls):
        return "crm-pc"


crm_pc_service = CrmPcService()
from agile.crm.apis.staff import Add, Get, Update, Search
crm_pc_service.add(Add, Get, Update, Search)

from agile.crm.apis.staff.myself import Get, Update
crm_pc_service.add(Get, Update)

# from agile.apis.staff.token import Renew
# crm_pc_service.add(Renew)

from agile.crm.apis.staff.account import Login, Logout
crm_pc_service.add(Login, Logout)

from agile.crm.apis.staff.account.vcode import Phone, Image
crm_pc_service.add(Phone, Image)

from agile.crm.apis.staff.account.password import Modify
crm_pc_service.add(Modify)

from agile.crm.apis.customer import Get, Search, Update, Add
crm_pc_service.add(Get, Search, Update, Add)

from agile.crm.apis.customer.bankcard import Search
crm_pc_service.add(Search)

from agile.crm.apis.customer.address import Search
crm_pc_service.add(Search)

from agile.crm.apis.customer.transaction import Search
crm_pc_service.add(Search)

from agile.crm.apis.production.brand import Get, Search, SearchAll, Update, \
                                            Add, Remove
crm_pc_service.add(Search, SearchAll, Get, Update, Add, Remove)

from agile.crm.apis.production import Get, Search, Update, Add, Remove, SearchAll
crm_pc_service.add(Search, Get, Update, Add, Remove, SearchAll)

from agile.crm.apis.university.major import Search, SearchAll, Add, Update, \
                                            Remove, Settop
crm_pc_service.add(Search, SearchAll, Add, Update, Remove, Settop)

from agile.crm.apis.university.school import Search, SearchAll, Add, Update, \
                                             Remove, Settop
crm_pc_service.add(Search, SearchAll, Add, Update, Remove, Settop)

from agile.crm.apis.tool.sms import Search
crm_pc_service.add(Search)

from agile.crm.apis.production.goods import Search, Add, Get, Update, Remove, Setuse
crm_pc_service.add(Search, Add, Get, Update, Remove, Setuse)

from agile.crm.apis.order import Get
crm_pc_service.add(Get)