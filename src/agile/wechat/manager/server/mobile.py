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
