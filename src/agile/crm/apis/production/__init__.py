# coding=UTF-8

import json
from infrastructure.core.field.base import CharField,DictField,\
        IntField,ListField,DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField,RequestFieldSet
from infrastructure.core.api.response import ResponseField,ResponseFieldSet

from agile.crm.manager.api import StaffAuthorizedApi
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.enterprise.manager import EnterpriseServer


class Get(StaffAuthorizedApi):

    request=with_metaclass(RequestFieldSet)
    request.production_id=RequestField(IntField,desc="产品id")

    response=with_metaclass(ResponseFieldSet)
    response.production_info=ResponseField(
        DictField,
        desc="产品信息",
        conf={
            'id': IntField(desc="产品id"),
            'name': CharField(desc="产品名称"),
            'description': CharField(desc="产品描述"),
            'attribute_list': ListField(
                desc="属性列表",
                fmt=DictField(
                    desc="分类信息",
                    conf={
                        'category': CharField(desc="分类名称"),
                        'attribute_list': ListField(
                            desc="分类名称",
                            fmt=DictField(
                                desc="属性标签",
                                conf={
                                    'name': CharField(desc="属性名称"),
                                }
                            )
                        ),
                    }
                )
            ),
            'workflow_list': ListField(
                desc="工作流列表",
                fmt=DictField(
                    desc="工作流信息",
                    conf={
                        'name': CharField(desc="名称"),
                        'type': CharField(desc="类型"),
                        'description': CharField(desc="描述"),
                    }
                )
            ),
            'brand_id': IntField(desc="品牌Id"),
            'brand_name': CharField(desc="品牌名称"),
            'company_id': IntField(desc="所属公司"),
            'update_time': DatetimeField(desc="更新时间"),
            'create_time': DatetimeField(desc="创建时间"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取产品信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        production=ProductionServer.get(
            request.production_id
        )
        return production

    def fill(self,response,production):
        response.production_info={
            'id': production.id,
            'name': production.name,
            'description': production.description,
            'attribute_list': json.loads(production.attribute_list),
            'workflow_list': json.loads(production.workflow_list),
            'brand_id': production.brand.id,
            'brand_name': production.brand.name,
            'company_id': production.company_id,
            'update_time': production.update_time,
            'create_time': production.create_time,
        }
        return response


class Search(StaffAuthorizedApi):
    request=with_metaclass(RequestFieldSet)
    request.current_page=RequestField(IntField,desc="当前页面")
    request.search_info=RequestField(
        DictField,
        desc="搜索产品",
        conf={
              'name': CharField(desc="产品名称",is_required=False),
        }
    )

    response=with_metaclass(ResponseFieldSet)
    response.total=ResponseField(IntField,desc="数据总数")
    response.total_page=ResponseField(IntField,desc="总页码数")
    response.data_list=ResponseField(
        ListField,
        desc="产品列表",
        fmt=DictField(
            desc="产品内容",
            conf={
                'id': IntField(desc="产品id"),
                'name': CharField(desc="产品名称"),
                'description': CharField(desc="产品描述"),
                'attribute_list': ListField(
                    desc="属性列表",
                    fmt=DictField(
                        desc="分类信息",
                        conf={
                            'category': CharField(desc="分类名称"),
                            'attribute_list': ListField(
                                desc="分类名称",
                                fmt=DictField(
                                    desc="属性标签",
                                    conf={
                                        'name': CharField(desc="属性名称"),
                                    }
                                )
                            ),
                        }
                    )
                ),
                'workflow_list': ListField(
                    desc="工作流列表",
                    fmt=DictField(
                        desc="工作流信息",
                        conf={
                            'name': CharField(desc="名称"),
                            'type': CharField(desc="类型"),
                            'description': CharField(desc="描述"),
                        }
                    )
                ),
                'brand_id': IntField(desc="品牌Id"),
                'brand_name': CharField(desc="品牌名称"),
                'company_id': IntField(desc="所属公司"),
                'update_time': DatetimeField(desc="更新时间"),
                'create_time': DatetimeField(desc="创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "产品搜索"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        company=EnterpriseServer.get_crm__company()
        spliter=ProductionServer.search(
            request.current_page,
            company.id,
            **request.search_info
        )
        return spliter

    def fill(self,response,production_spliter):
        data_list=[{
            'id': production.id,
            'name': production.name,
            'description': production.description,
            'attribute_list': json.loads(production.attribute_list),
            'workflow_list': json.loads(production.workflow_list),
            'brand_id': production.brand.id,
            'brand_name': production.brand.name,
            'company_id': production.company_id,
            'update_time': production.update_time,
            'create_time': production.create_time,
        } for production in production_spliter.data]
        response.data_list=data_list
        response.total=production_spliter.total
        response.total_page=production_spliter.total_page
        return response


class Add(StaffAuthorizedApi):
    request=with_metaclass(RequestFieldSet)
    request.brand_id=RequestField(IntField,desc="品牌Id")
    request.production_info=RequestField(
        DictField,
        desc="产品信息",
        conf={
            'name': CharField(desc="产品名称"),
            'description': CharField(desc="产品描述"),
            'attribute_list': ListField(
                desc="属性列表",
                fmt=DictField(
                    desc="分类信息",
                    conf={
                        'category': CharField(desc="分类名称"),
                        'attribute_list': ListField(
                            desc="分类名称",
                            fmt=DictField(
                                desc="属性标签",
                                conf={
                                    'name': CharField(desc="属性名称"),
                                }
                            )
                        ),
                    }
                )
            ),
            'workflow_list': ListField(
                desc="工作流列表",
                fmt=DictField(
                    desc="工作流信息",
                    conf={
                        'name': CharField(desc="名称"),
                        'type': CharField(desc="类型"),
                        'description': CharField(desc="描述"),
                    }
                )
            )
        }
    )

    response=with_metaclass(ResponseFieldSet)
    response.production_id=ResponseField(IntField,desc="产品ID")

    @classmethod
    def get_desc(cls):
        return "创建产品"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        company=EnterpriseServer.get_crm__company()
        add_info=request.production_info
        add_info.attribute_list=json.dumps(add_info.attribute_list)
        add_info.workflow_list=json.dumps(add_info.workflow_list)
        production=ProductionServer.generate(
            company_id=company.id,
            brand_id=request.brand_id,
            **add_info
        )
        return production

    def fill(self,response,production):
        response.production_id=production.id
        return response


class Update(StaffAuthorizedApi):
    request=with_metaclass(RequestFieldSet)
    request.production_id=RequestField(IntField,desc="产品id")
    request.update_info=RequestField(
        DictField,
        desc="需要更新的产品信息",
        conf={
            'name': CharField(desc="产品名称"),
            'description': CharField(desc="产品描述"),
            'attribute_list': ListField(
                desc="属性列表",
                fmt=DictField(
                    desc="分类信息",
                    conf={
                        'category': CharField(desc="分类名称"),
                        'attribute_list': ListField(
                            desc="分类名称",
                            fmt=DictField(
                                desc="属性标签",
                                conf={
                                    'name': CharField(desc="属性名称"),
                                }
                            )
                        ),
                    }
                )
            ),
            'workflow_list': ListField(
                desc="工作流列表",
                fmt=DictField(
                    desc="工作流信息",
                    conf={
                        'name': CharField(desc="名称"),
                        'type': CharField(desc="类型"),
                        'description': CharField(desc="描述"),
                    }
                )
            )
        }
    )

    response=with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "更新产品"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self,request):
        update_info=request.update_info
        update_info.attribute_list=json.dumps(update_info.attribute_list)
        update_info.workflow_list=json.dumps(update_info.workflow_list)
        ProductionServer.update(
            production_id=request.production_id,
            **update_info
        )

    def fill(self,response,address_list):
        return response


class Remove(StaffAuthorizedApi):
    """删除产品信息"""
    request=with_metaclass(RequestFieldSet)
    request.production_id=RequestField(IntField,desc="产品id")


    response=with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "产品信息删除接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self,request):
        ProductionServer.delete(
            request.production_id,
        )

    def fill(self,response):
        return response