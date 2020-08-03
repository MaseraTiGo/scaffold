# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''

import json

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.middleground.business.transaction.utils.constant import \
        PayTypes, PayService
from abs.middleground.business.merchandise.utils.constant import \
        DespatchService, UseStatus
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.merchandise.manager import MerchandiseServer


class Add(NoAuthorizedApi):
    """
    添加商品
    """
    request = with_metaclass(RequestFieldSet)
    request.merchandise_info = RequestField(
        DictField,
        desc="商品详情",
        conf={
            'title': CharField(desc="标题"),
            'video_display': CharField(desc="宣传视频"),
            'description': CharField(desc="描述"),
            'slideshow': ListField(
                desc='轮播图',
                fmt=CharField(desc="图片地址")
            ),
            'detail': ListField(
                desc='详情页',
                fmt=CharField(desc="图片地址")
            ),
            'pay_types': ListField(
                desc='详情页',
                fmt=CharField(desc="支付方式", choices=PayTypes.CHOICES)
            ),
            'pay_services': ListField(
                desc='详情页',
                fmt=CharField(desc="支付服务", choices=PayService.CHOICES)
            ),
            'market_price': IntField(desc="市场价, 单位:分"),
            'despatch_type': CharField(
                desc="发货方式",
                choices=DespatchService.CHOICES
            ),
            'company_id': IntField(desc="公司ID"),
            'production_id': IntField(desc="产品ID"),
            'remark': CharField(desc="备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.merchandise_id = ResponseField(IntField, desc="商品Id")

    @classmethod
    def get_desc(cls):
        return "添加商品接口(添加商品时，不能控制上下架状态)"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        merchandise_info = request.merchandise_info
        merchandise_info.slideshow = json.dumps(merchandise_info.slideshow)
        merchandise_info.detail = json.dumps(merchandise_info.detail)
        merchandise_info.pay_types = json.dumps(merchandise_info.pay_types)
        merchandise_info.pay_services = json.dumps(
            merchandise_info.pay_services
        )
        EnterpriseServer.get(merchandise_info.company_id)
        ProductionServer.get(merchandise_info.production_id)
        merchandise = MerchandiseServer.generate(
            **merchandise_info
        )
        return merchandise

    def fill(self, response, merchandise):
        response.merchandise_id = merchandise.id
        return response


class Search(NoAuthorizedApi):
    """
    搜索商品
    """
    request = with_metaclass(RequestFieldSet)
    request.company_id = RequestField(
        IntField,
        desc="当前页码"
    )
    request.current_page = RequestField(
        IntField,
        desc="当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc="搜索商品条件",
        conf={
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="商品列表",
        fmt=DictField(
            desc="商品详情",
            conf={
                'id': IntField(desc="编号"),
                'title': CharField(desc="标题"),
                'video_display': CharField(desc="宣传视频"),
                'description': CharField(desc="描述"),
                'slideshow': ListField(
                    desc='轮播图',
                    fmt=CharField(desc="图片地址")
                ),
                'detail': ListField(
                    desc='详情页',
                    fmt=CharField(desc="图片地址")
                ),
                'pay_types': ListField(
                    desc='详情页',
                    fmt=CharField(desc="支付方式", choices=PayTypes.CHOICES)
                ),
                'pay_services': ListField(
                    desc='详情页',
                    fmt=CharField(desc="支付服务", choices=PayService.CHOICES)
                ),
                'market_price': IntField(desc="市场价, 单位:分"),
                'despatch_type': CharField(
                    desc="发货方式",
                    choices=DespatchService.CHOICES
                ),
                'use_status': CharField(
                    desc="使用状态",
                    choices=UseStatus.CHOICES
                ),
                'company_id': IntField(desc="公司ID"),
                'production_id': IntField(desc="产品ID"),
                'remark': CharField(desc="备注"),
                'specification_list': ListField(
                    desc="规格列表",
                    fmt=DictField(
                        desc="规格详情",
                        conf={
                            "id": IntField(desc="规格id"),
                            "show_image": CharField(desc="展示图片"),
                            "sale_price": IntField(desc="销售价为，单位：分"),
                            "stock": IntField(desc="库存"),
                            "remark": CharField(desc="备注"),
                            "specification_value_list": ListField(
                                desc="属性值列表",
                                fmt=DictField(
                                    desc="属性详情",
                                    conf={
                                        "category": CharField(desc="属性分类"),
                                        "attribute": IntField(desc="属性值"),
                                    }
                                )
                            ),
                        }
                    )
                )
            }
        )
    )
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "搜索商品"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        merchandise_spliter = MerchandiseServer.search(
            request.current_page,
            request.company_id,
            **request.search_info
        )
        return merchandise_spliter

    def fill(self, response, merchandise_spliter):
        data_list = [{
            'id': merchandise.id,
            'title': merchandise.title,
            'video_display': merchandise.video_display,
            'description': merchandise.description,
            'slideshow': json.loads(merchandise.slideshow),
            'detail': json.loads(merchandise.detail),
            'pay_types': json.loads(merchandise.pay_types),
            'pay_services': json.loads(merchandise.pay_services),
            'market_price': merchandise.market_price,
            'despatch_type': merchandise.despatch_type,
            'company_id': merchandise.company_id,
            'production_id': merchandise.production_id,
            'use_status': merchandise.use_status,
            'remark': merchandise.remark,
            'specification_list': [{
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
            } for specification in merchandise.specification_list]
        } for merchandise in merchandise_spliter.data]
        response.data_list = data_list
        response.total = merchandise_spliter.total
        response.total_page = merchandise_spliter.total_page
        return response


class Get(NoAuthorizedApi):
    """
    获取商品详情接口
    """
    request = with_metaclass(RequestFieldSet)
    request.merchandise_id = RequestField(IntField, desc="商品id")

    response = with_metaclass(ResponseFieldSet)
    response.merchandise_info = ResponseField(
        DictField,
        desc="商品详情",
        conf={
            'id': IntField(desc="编号"),
            'title': CharField(desc="标题"),
            'video_display': CharField(desc="宣传视频"),
            'description': CharField(desc="描述"),
            'slideshow': ListField(
                desc='轮播图',
                fmt=CharField(desc="图片地址")
            ),
            'detail': ListField(
                desc='详情页',
                fmt=CharField(desc="图片地址")
            ),
            'pay_types': ListField(
                desc='详情页',
                fmt=CharField(desc="支付方式", choices=PayTypes.CHOICES)
            ),
            'pay_services': ListField(
                desc='详情页',
                fmt=CharField(desc="支付服务", choices=PayService.CHOICES)
            ),
            'market_price': IntField(desc="市场价, 单位:分"),
            'despatch_type': CharField(
                desc="发货方式",
                choices=DespatchService.CHOICES
            ),
            'use_status': CharField(
                desc="使用状态",
                choices=UseStatus.CHOICES
            ),
            'company_id': IntField(desc="公司ID"),
            'production_id': IntField(desc="产品ID"),
            'remark': CharField(desc="备注"),
            'specification_list': ListField(
                desc="规格列表",
                fmt=DictField(
                    desc="规格详情",
                    conf={
                        "id": IntField(desc="规格id"),
                        "show_image": CharField(desc="展示图片"),
                        "sale_price": IntField(desc="销售价为，单位：分"),
                        "stock": IntField(desc="库存"),
                        "remark": CharField(desc="备注"),
                        "specification_value_list": ListField(
                            desc="属性值列表",
                            fmt=DictField(
                                desc="属性详情",
                                conf={
                                    "category": CharField(desc="属性分类"),
                                    "attribute": IntField(desc="属性值"),
                                }
                            )
                        ),
                    }
                )
            )
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取商品详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return MerchandiseServer.get(request.merchandise_id)

    def fill(self, response, merchandise):
        response.merchandise_info = {
            'id': merchandise.id,
            'title': merchandise.title,
            'video_display': merchandise.video_display,
            'description': merchandise.description,
            'slideshow': json.loads(merchandise.slideshow),
            'detail': json.loads(merchandise.detail),
            'pay_types': json.loads(merchandise.pay_types),
            'pay_services': json.loads(merchandise.pay_services),
            'market_price': merchandise.market_price,
            'despatch_type': merchandise.despatch_type,
            'company_id': merchandise.company_id,
            'production_id': merchandise.production_id,
            'use_status': merchandise.use_status,
            'remark': merchandise.remark,
            'specification_list': [{
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
            } for specification in merchandise.specification_list]
        }
        return response


class Update(NoAuthorizedApi):
    """
    修改商品信息
    """
    request = with_metaclass(RequestFieldSet)
    request.merchandise_id = RequestField(IntField, desc="商品id")
    request.update_info = RequestField(
        DictField,
        desc="商品修改详情",
        conf={
            'title': CharField(desc="标题"),
            'video_display': CharField(desc="宣传视频"),
            'slideshow': ListField(
                desc='轮播图',
                fmt=CharField(desc="图片地址")
            ),
            'detail': ListField(
                desc='详情页',
                fmt=CharField(desc="图片地址")
            ),
            'pay_types': ListField(
                desc='详情页',
                fmt=CharField(desc="支付方式", choices=PayTypes.CHOICES)
            ),
            'pay_services': ListField(
                desc='详情页',
                fmt=CharField(desc="支付服务", choices=PayService.CHOICES)
            ),
            'market_price': IntField(desc="市场价, 单位:分"),
            'despatch_type': CharField(
                desc="发货方式",
                choices=DespatchService.CHOICES
            ),
            'use_status': CharField(
                desc="使用状态",
                choices=UseStatus.CHOICES
            ),
            'company_id': IntField(desc="公司ID"),
            'production_id': IntField(desc="产品ID"),
            'remark': CharField(desc="备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "商品个人中心修改接口（仅修改商品基础属性）"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        update_info = request.update_info
        update_info.slideshow = json.dumps(update_info.slideshow)
        update_info.detail = json.dumps(update_info.detail)
        update_info.pay_types = json.dumps(update_info.pay_types)
        update_info.pay_services = json.dumps(
            update_info.pay_services
        )
        EnterpriseServer.get(update_info.company_id)
        ProductionServer.get(update_info.production_id)
        MerchandiseServer.update(
            request.merchandise_id,
            **update_info
        )

    def fill(self, response):
        return response


class Remove(NoAuthorizedApi):
    """
    删除商品信息
    """
    request = with_metaclass(RequestFieldSet)
    request.merchandise_id = RequestField(IntField, desc="商品id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除商品"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        MerchandiseServer.remove(
            request.merchandise_id
        )

    def fill(self, response):
        return response
