# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
    IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.adsense.manager import SpaceServer, AdvertisementServer


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.space_info = RequestField(
        DictField,
        desc="广告位信息",
        conf={
            'label': CharField(desc="广告位标签"),
            'name': CharField(desc="广告位名称"),
            'width': IntField(desc="宽度"),
            'height': CharField(desc="高度"),
            'is_enable': BooleanField(desc="开关")
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.space_id = ResponseField(IntField, desc="广告ID")

    @classmethod
    def get_desc(cls):
        return "广告位添加接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        if SpaceServer.get_bylabel(request.space_info['label']):
            raise BusinessError('标签重复')
        space = SpaceServer.create(
            **request.space_info
        )
        return space

    def fill(self, response, space):
        response.space_id = space.id
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.space_id = RequestField(IntField, desc="广告位id")
    request.space_info = RequestField(
        DictField,
        desc="广告位信息",
        conf={
            'label': CharField(desc="广告位标签", is_required=False),
            'name': CharField(desc="广告位名称", is_required=False),
            'width': IntField(desc="宽度", is_required=False),
            'height': CharField(desc="高度", is_required=False),
            'is_enable': BooleanField(desc="开关", is_required=False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.space_id = ResponseField(IntField, desc="广告ID")

    @classmethod
    def get_desc(cls):
        return "广告添加接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        if 'label' in request.space_info:
            check_space = SpaceServer.get_bylabel(request.space_info['label'])
            if check_space and check_space.id != request.space_id:
                raise BusinessError('标签重复')
        space = SpaceServer.get(request.space_id)
        space.update(**request.space_info)
        return space

    def fill(self, response, space):
        response.space_id = space.id
        return response


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页面")
    request.search_info = RequestField(
        DictField,
        desc="搜索广告位",
        conf={
            'name': CharField(desc="广告名称", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="广告位列表",
        fmt=DictField(
            desc="广告位内容",
            conf={
                'id': IntField(desc="id"),
                'label': CharField(desc="广告位标签"),
                'name': CharField(desc="广告位名称"),
                'width': IntField(desc="宽度"),
                'height': CharField(desc="高度"),
                'is_enable': BooleanField(desc="开关"),
                'enable_num': IntField(desc="展示广告数"),
                'create_time': DatetimeField(desc="创建时间")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "广告位搜索接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        spliter = SpaceServer.search(
            request.current_page,
            **request.search_info
        )
        AdvertisementServer.hung_enable_num(spliter.data)
        return spliter

    def fill(self, response, spliter):
        data_list = [{
            'id': space.id,
            'label': space.label,
            'name': space.name,
            'width': space.width,
            'height': space.height,
            'is_enable': space.is_enable,
            'enable_num': space.enable_num,
            'create_time': space.create_time
        } for space in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class SearchAll(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="广告位列表",
        fmt=DictField(
            desc="广告位内容",
            conf={
                'id': IntField(desc="id"),
                'label': CharField(desc="广告位标签"),
                'name': CharField(desc="广告位名称"),
                'width': IntField(desc="宽度"),
                'height': CharField(desc="高度"),
                'is_enable': BooleanField(desc="开关")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "广告位搜索接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        data_list = SpaceServer.search_all()
        return data_list

    def fill(self, response, data_list):
        data_list = [{
            'id': space.id,
            'label': space.label,
            'name': space.name,
            'width': space.width,
            'height': space.height,
            'is_enable': space.is_enable
        } for space in data_list]
        response.data_list = data_list
        return response
