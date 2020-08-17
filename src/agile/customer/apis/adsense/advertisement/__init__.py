# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.services.crm.adsense.manager import AdvertisementServer


class Search(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(
        DictField,
        desc="搜索广告",
        conf={
            'label': CharField(desc="广告位标签")
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="广告列表",
        fmt=DictField(
            desc="广告内容",
            conf={
                'id': IntField(desc="广告id"),
                'name': CharField(desc="广告名称"),
                'thumbnail': CharField(desc="广告缩略图"),
                'url': CharField(desc="跳转地址")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "广告接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        ad_list = AdvertisementServer.search_all(
            **request.search_info
        )
        return ad_list

    def fill(self, response, ad_list):
        data_list = [{
            'id': ad.id,
            'name': ad.name,
            'thumbnail': ad.thumbnail,
            'url': ad.url
        } for ad in ad_list]
        response.data_list = data_list
        return response
