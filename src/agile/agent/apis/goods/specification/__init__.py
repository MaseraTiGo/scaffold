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
from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.services.agent.goods.manager import GoodsServer


class Add(AgentStaffAuthorizedApi):
    """
    添加商品规格
    """
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")
    request.specification_list = RequestField(
        ListField,
        desc = "规格列表",
        fmt = DictField(
            desc = "商品规格内容",
            conf = {
                'show_image': CharField(desc = "图片"),
                'sale_price': IntField(desc = "销售价/分"),
                'stock': IntField(desc = "库存"),
                "specification_value_list": ListField(
                    desc = "属性值列表",
                    fmt = DictField(
                        desc = "属性详情",
                        conf = {
                            "category": CharField(desc = "属性分类"),
                            "attribute": CharField(desc = "属性值"),
                        }
                    )
                ),
            }
        )
    )


    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加商品规格接口(添加商品规格时，不能控制上下架状态)"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        for specification in request.specification_list:
            specification_info = {
                "merchandise_id":goods.merchandise_id,
                "show_image" : specification["show_image"],
                "sale_price" : specification["sale_price"],
                "stock" : specification["stock"],
                "remark" : "",
                "attribute_list":specification["specification_value_list"],
            }
            MerchandiseServer.generate_specification(**specification_info)

    def fill(self, response,):
        return response


class Get(AgentStaffAuthorizedApi):
    """
    获取商品规格详情接口
    """
    request = with_metaclass(RequestFieldSet)
    request.specification_id = RequestField(IntField, desc = "商品规格id")

    response = with_metaclass(ResponseFieldSet)
    response.specification_info = ResponseField(
        DictField,
        desc = "商品规格详情",
        conf = {
            'id': IntField(desc = "编号"),
            'show_image': CharField(desc = "图片"),
            'sale_price': IntField(desc = "销售价"),
            'stock': IntField(desc = "库存"),
            'remark': CharField(desc = "备注"),
            'specification_value_list': ListField(
                desc = '属性列表',
                fmt = DictField(
                    desc = "属性",
                    conf = {
                        'category': CharField(desc = "属性分类"),
                        'attribute': CharField(desc = "属性"),
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


class Update(AgentStaffAuthorizedApi):
    """
    修改商品规格信息
    """
    request = with_metaclass(RequestFieldSet)
    request.specification_id = RequestField(IntField, desc = "商品规格id")
    request.update_info = RequestField(
        DictField,
        desc = "商品规格修改详情",
        conf = {
            'show_image': CharField(desc = "图片"),
            'sale_price': IntField(desc = "销售价"),
            'stock': IntField(desc = "库存"),
            'remark': CharField(desc = "备注", is_required = False),
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


class Remove(AgentStaffAuthorizedApi):
    """
    删除商品规格信息
    """
    request = with_metaclass(RequestFieldSet)
    request.specification_id = RequestField(IntField, desc = "商品规格id")

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
