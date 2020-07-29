# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService


class CustomerMobileService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "客户服务"

    @classmethod
    def get_desc(self):
        return "针对客户提供的相关的服务"

    @classmethod
    def get_flag(cls):
        return "customer-mobile"


customer_mobile_service = CustomerMobileService()
from agile.customer.apis.customer.account import Login, Logout, Register, CodeLogin
customer_mobile_service.add(Register, Login, Logout, CodeLogin)

from agile.customer.apis.customer.account.vcode import Phone, Image
customer_mobile_service.add(Phone, Image)

from agile.customer.apis.customer.account.password import Forget, Modify
customer_mobile_service.add(Forget, Modify)

from agile.customer.apis.customer.account.token import Renew
customer_mobile_service.add(Renew)

from agile.customer.apis.customer.myself import Get, Update
customer_mobile_service.add(Get, Update)

from agile.customer.apis.customer.myself.address import Get, All, Remove, Add, Update
customer_mobile_service.add(Add, Get, All, Update, Remove)

from agile.customer.apis.customer.myself.bankcard import Get, All, Remove, Add
customer_mobile_service.add(Add, Get, All, Remove)

from agile.customer.apis.customer.myself.real import Authenticate, Get
customer_mobile_service.add(Authenticate, Get)

from agile.customer.apis.customer.finance.balance import Get, TopUp, Withdraw
customer_mobile_service.add(Get, TopUp, Withdraw)

from agile.customer.apis.customer.finance.transaction import Get, Search
customer_mobile_service.add(Get, Search)

from agile.customer.apis.customer.finance.transaction.statistics import Monthly
customer_mobile_service.add(Monthly)

from agile.customer.apis.university.school import HotSearch, Search, All
customer_mobile_service.add(HotSearch, Search, All)

from agile.customer.apis.university.major import All
customer_mobile_service.add(All)

from agile.customer.apis.production.goods import Search
customer_mobile_service.add(Search)
