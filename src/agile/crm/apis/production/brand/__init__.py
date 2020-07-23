# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.crm.manager.api import StaffAuthorizedApi
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.production.utils.constant import IndustryTypes
from abs.middleground.business.enterprise.manager import EnterpriseServer


class Get(StaffAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.brand_id = RequestField(IntField, desc="品牌id")

    response = with_metaclass(ResponseFieldSet)
    response.brand_info = ResponseField(
        DictField,
        desc="品牌信息",
        conf={
            'id': IntField(desc="品牌id"),
            'name': CharField(desc="品牌名称"),
            'industry': CharField(
                desc="所处行业",
                choices=IndustryTypes.CHOICES
            ),
            'description': CharField(desc="品牌描述"),
            'company_id': IntField(desc="所属公司"),
            'create_time': DatetimeField(desc="创建时间"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取品牌信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        brand = ProductionServer.get_brand(
            request.brand_id
        )
        return brand

    def fill(self, response, brand):
        response.brand_info = {
            'id': brand.id,
            'name': brand.name,
            'industry': brand.industry,
            'description': brand.description,
            'company_id': brand.company_id,
            'create_time': brand.create_time,
        }
        return response


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页面")
    request.search_info = RequestField(
        DictField,
        desc="搜索品牌",
        conf={
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="品牌列表",
        fmt=DictField(
            desc="品牌内容",
            conf={
                'id': IntField(desc="品牌id"),
                'name': CharField(desc="品牌名称"),
                'industry': CharField(
                    desc="所处行业",
                    choices=IndustryTypes.CHOICES
                ),
                'description': CharField(desc="品牌描述"),
                'company_id': IntField(desc="所属公司"),
                'create_time': DatetimeField(desc="创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "品牌搜索"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        company = EnterpriseServer.get_crm__company()
        spliter = ProductionServer.search_brand(
            request.current_page,
            company.id,
            **request.search_info
        )
        return spliter

    def fill(self, response, brand_spliter):
        data_list = [{
            'id': brand.id,
            'name': brand.name,
            'industry': brand.industry,
            'description': brand.description,
            'company_id': brand.company_id,
            'create_time': brand.create_time,
        } for brand in brand_spliter.data]
        response.data_list = data_list
        response.total = brand_spliter.total
        response.total_page = brand_spliter.total_page
        return response


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.brand_info = RequestField(
        DictField,
        desc="品牌信息",
        conf={
            'name': CharField(desc="品牌名称"),
            'industry': CharField(
                desc="所处行业",
                choices=IndustryTypes.CHOICES
            ),
            'description': CharField(desc="品牌描述"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.brand_id = ResponseField(IntField, desc="品牌ID")

    @classmethod
    def get_desc(cls):
        return "创建品牌"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        company = EnterpriseServer.get_crm__company()
        brand = ProductionServer.generate_brand(
            company_id=company.id,
            **request.brand_info
        )
        return brand

    def fill(self, response, brand):
        response.brand_id = brand.id
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.brand_id = RequestField(IntField, desc="品牌id")
    request.update_info = RequestField(
        DictField,
        desc="需要更新的品牌信息",
        conf={
            'name': CharField(desc="品牌名称"),
            'industry': CharField(
                desc="所处行业",
                choices=IndustryTypes.CHOICES
            ),
            'description': CharField(desc="品牌描述"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "更新品牌"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        ProductionServer.update_brand(
            request.brand_id,
            **request.update_info
        )

    def fill(self, response, address_list):
        return response
