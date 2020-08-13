# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''


from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.middleground.business.merchandise.manager import MerchandiseServer


class Add(NoAuthorizedApi):
    """
    添加商品规格
    """
    request = with_metaclass(RequestFieldSet)
    request.merchandise_id = RequestField(IntField, desc="商品id")
    request.specification_info = RequestField(
        DictField,
        desc="商品规格详情",
        conf={
            'show_image': CharField(desc="图片"),
            'sale_price': IntField(desc="销售价"),
            'stock': IntField(desc="库存"),
            'remark': CharField(desc="备注"),
            'attribute_list': ListField(
                desc='属性列表',
                fmt=DictField(
                    desc="属性",
                    conf={
                        'category': CharField(desc="属性分类"),
                        'attribute': CharField(desc="属性"),
                    }
                )
            ),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.specification_id = ResponseField(IntField, desc="商品规格Id")

    @classmethod
    def get_desc(cls):
        return "添加商品规格接口(添加商品规格时，不能控制上下架状态)"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        specification_info = request.specification_info
        specification = MerchandiseServer.generate_specification(
            request.merchandise_id,
            **specification_info
        )
        return specification

    def fill(self, response, specification):
        response.specification_id = specification.id
        return response


class Get(NoAuthorizedApi):
    """
    获取商品规格详情接口
    """
    request = with_metaclass(RequestFieldSet)
    request.specification_id = RequestField(IntField, desc="商品规格id")

    response = with_metaclass(ResponseFieldSet)
    response.specification_info = ResponseField(
        DictField,
        desc="商品规格详情",
        conf={
            'id': IntField(desc="编号"),
            'show_image': CharField(desc="图片"),
            'sale_price': IntField(desc="销售价"),
            'stock': IntField(desc="库存"),
            'remark': CharField(desc="备注"),
            'specification_value_list': ListField(
                desc='属性列表',
                fmt=DictField(
                    desc="属性",
                    conf={
                        'category': CharField(desc="属性分类"),
                        'attribute': CharField(desc="属性"),
                    }
                )
            ),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取商品规格详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return MerchandiseServer.get_specification(request.specification_id)

    def fill(self, response, specification):
        response.specification_info = {
            'id': specification.id,
            'show_image': specification.show_image,
            'sale_price': specification.sale_price,
            'stock': specification.stock,
            'remark': specification.remark,
            'specification_value_list': [
                {
                    "category": sv.category,
                    "attribute": sv.attribute,
                }
                for sv in specification.specification_value_list
            ],
        }
        return response


class Update(NoAuthorizedApi):
    """
    修改商品规格信息
    """
    request = with_metaclass(RequestFieldSet)
    request.specification_id = RequestField(IntField, desc="商品规格id")
    request.update_info = RequestField(
        DictField,
        desc="商品规格修改详情",
        conf={
            'show_image': CharField(desc="图片"),
            'sale_price': IntField(desc="销售价"),
            'stock': IntField(desc="库存"),
            'remark': CharField(desc="备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "商品规格个人中心修改接口(不更新属性)"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        MerchandiseServer.update_specification(
            request.specification_id,
            **request.update_info
        )

    def fill(self, response):
        return response


class Remove(NoAuthorizedApi):
    """
    删除商品规格信息
    """
    request = with_metaclass(RequestFieldSet)
    request.specification_id = RequestField(IntField, desc="商品规格id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除商品规格"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        MerchandiseServer.remove_specification(
            request.specification_id
        )

    def fill(self, response):
        return response
