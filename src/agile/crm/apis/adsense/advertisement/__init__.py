# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.adsense.manager import AdvertisementServer, SpaceServer


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.ad_info = RequestField(
        DictField,
        desc="广告信息",
        conf={
            'space_id_list': ListField(
                desc="广告位id列表",
                fmt=IntField('广告位id')
            ),
            'name': CharField(desc="广告名称"),
            'thumbnail': CharField(desc="广告缩略图"),
            'url': CharField(desc="跳转地址"),
            'sort': IntField(desc="排序"),
            'is_enable': BooleanField(desc="开关", is_required=False)
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "广告添加接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        space_list = SpaceServer.search_all(
            id__in=request.ad_info.pop('space_id_list')
        )
        AdvertisementServer.bulk_create(
            space_list,
            **request.ad_info
        )

    def fill(self, response):
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.ad_id = RequestField(IntField, desc="广告id")
    request.ad_info = RequestField(
        DictField,
        desc="广告信息",
        conf={
            'name': CharField(desc="广告名称", is_required=False),
            'thumbnail': CharField(desc="广告缩略图", is_required=False),
            'url': CharField(desc="跳转地址", is_required=False),
            'sort': IntField(desc="排序", is_required=False),
            'is_enable': BooleanField(desc="开关", is_required=False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.ad_id = ResponseField(IntField, desc="广告ID")

    @classmethod
    def get_desc(cls):
        return "广告添加接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        ad = AdvertisementServer.get(request.ad_id)
        ad.update(**request.ad_info)
        return ad

    def fill(self, response, ad):
        response.ad_id = ad.id
        return response


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页面")
    request.search_info = RequestField(
        DictField,
        desc="搜索广告",
        conf={
            'name': CharField(desc="广告名称", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="广告列表",
        fmt=DictField(
            desc="广告内容",
            conf={
                'id': IntField(desc="广告id"),
                'space_id': IntField(desc="广告位id"),
                'space_name': CharField(desc="广告位名称"),
                'name': CharField(desc="广告名称"),
                'thumbnail': CharField(desc="广告缩略图"),
                'url': CharField(desc="跳转地址"),
                'sort': IntField(desc="排序"),
                'is_enable': BooleanField(desc="开关"),
                'create_time': DatetimeField(desc="创建时间")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "广告搜索接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        spliter = AdvertisementServer.search(
            request.current_page,
            **request.search_info
        )
        return spliter

    def fill(self, response, spliter):
        data_list = [{
            'id': ad.id,
            'space_id': ad.space.id,
            'space_name': ad.space.name,
            'name': ad.name,
            'thumbnail': ad.thumbnail,
            'url': ad.url,
            'sort': ad.sort,
            'is_enable': ad.is_enable,
            'create_time': ad.create_time
        } for ad in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Remove(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.ad_id = RequestField(IntField, desc="广告id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "广告搜索接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        ad = AdvertisementServer.get(
            request.ad_id
        )
        ad.delete()

    def fill(self, response):
        return response
