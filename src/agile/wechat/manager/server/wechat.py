# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService


class CustomerWechatService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "客户服务"

    @classmethod
    def get_desc(self):
        return "针对客户提供的相关的服务"

    @classmethod
    def get_flag(cls):
        return "customer-wechat"


customer_wechat_service = CustomerWechatService()

from agile.wechat.apis.adsense.advertisement import Search
customer_wechat_service.add(Search)

from agile.wechat.apis.university.school import HotSearch, Search, All, Get, Location
customer_wechat_service.add(HotSearch, Search, All, Get, Location)

from agile.wechat.apis.university.major import All, Duration, HotSearch, Search, Get
customer_wechat_service.add(All, Duration, HotSearch, Search, Get)

from agile.wechat.apis.university.relations import SearchMajor, SearchSchool
customer_wechat_service.add(SearchMajor, SearchSchool)

from agile.wechat.apis.production.goods import Search, Get, HotSearch
customer_wechat_service.add(Search, Get, HotSearch)

from agile.wechat.apis.customer.account import AutoLogin, PhoneRegister, WechatRegister, Unbind
customer_wechat_service.add(AutoLogin, PhoneRegister, WechatRegister, Unbind)

from agile.wechat.apis.customer.account.vcode import Phone
customer_wechat_service.add(Phone)

from agile.wechat.apis.customer.account.vcode import Phone
customer_wechat_service.add(Phone)

from agile.wechat.apis.customer.account.password import Forget, Modify, SetUp
customer_wechat_service.add(Forget, Modify, SetUp)

from agile.wechat.apis.customer.myself import Get, Update
customer_wechat_service.add(Get, Update)

from agile.wechat.apis.customer.myself.address import Get, All, Remove, Add, Update
customer_wechat_service.add(Add, Get, All, Update, Remove)

from agile.wechat.apis.customer.myself.bankcard import Get, All, Remove, Add
customer_wechat_service.add(Add, Get, All, Remove)

from agile.wechat.apis.customer.myself.real import Authenticate, Get
customer_wechat_service.add(Authenticate, Get)

from agile.wechat.apis.customer.finance.balance import Get, TopUp, Withdraw
customer_wechat_service.add(Get, TopUp, Withdraw)

from agile.wechat.apis.customer.finance.transaction import Get, Search
customer_wechat_service.add(Get, Search)

from agile.wechat.apis.customer.finance.transaction.statistics import Monthly
customer_wechat_service.add(Monthly)

from agile.wechat.apis.customer.order import Add, Get, Search, Pay, Cancel, PosterAdd
customer_wechat_service.add(Add, Get, Search, Pay, Cancel, PosterAdd)

from agile.wechat.apis.customer.contract import Get, Search, Autograph
customer_wechat_service.add(Get, Search, Autograph)

from agile.wechat.apis.production.poster import Get
customer_wechat_service.add(Get)
