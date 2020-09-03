# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.crm.university.utils.constant import DurationTypes, \
     CategoryTypes
from abs.middleground.business.merchandise.utils.constant import\
     DespatchService, UseStatus

from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.middleground.business.production.manager import ProductionServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.crm.university.manager import UniversityServer, \
     UniversityYearsServer
from abs.services.crm.agent.manager import AgentServer
from abs.services.agent.order.manager import OrderItemServer


class Get(AgentStaffAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")


    response = with_metaclass(ResponseFieldSet)
    response.goods_info = ResponseField(
        DictField,
        desc = "商品详情",
        conf = {
            'title': CharField(desc = "标题"),
            'video_display': CharField(desc = "宣传视频"),
            'slideshow': ListField(
                desc = '轮播图',
                fmt = CharField(desc = "图片地址")
            ),
            'detail': ListField(
                desc = '详情页',
                fmt = CharField(desc = "图片地址")
            ),
            'market_price': IntField(desc = "市场价, 单位:分"),
            'despatch_type': CharField(
                desc = "发货方式",
                choices = DespatchService.CHOICES
            ),
            'production_id': IntField(desc = "产品ID"),
            'production_name': CharField(desc = "产品ID"),
            'school_id': IntField(desc = "学校ID"),
            'school_name': CharField(desc = "学校名称"),
            'major_id': IntField(desc = "专业ID"),
            'major_name': CharField(desc = "专业名称"),
            'description': CharField(desc = "商品描述"),
            'years_id': IntField(desc = "学年ID"),
            'duration':CharField(
                desc = "时长",
                choices = DurationTypes.CHOICES
            ),
            'category':CharField(
                desc = "分类",
                choices = CategoryTypes.CHOICES
            ),
            "use_status":CharField(
                desc = "上下架",
                choices = UseStatus.CHOICES,
            ),
            'remark': CharField(desc = "备注"),
            'specification_list': ListField(
                    desc = "规格列表",
                    fmt = DictField(
                        desc = "规格详情",
                        conf = {
                            'id': IntField(desc = "规格id"),
                            'show_image': CharField(desc = "图片"),
                            'sale_price': IntField(desc = "销售价/分"),
                            'original_price': IntField(desc = "原价"),
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
        }
    )

    @classmethod
    def get_desc(cls):
        return "商品信息查询接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        UniversityServer.hung_school([goods])
        UniversityServer.hung_major([goods])
        MerchandiseServer.hung_merchandise([goods])
        ProductionServer.hung_production([goods.merchandise])
        UniversityYearsServer.hung_years([goods])
        return goods

    def fill(self, response, goods):
        response.goods_info = {
            'id': goods.id,
            'title': goods.merchandise.title,
            'video_display': goods.merchandise.video_display,
            'slideshow': json.loads(goods.merchandise.slideshow),
            'detail': json.loads(goods.merchandise.detail),
            'market_price': goods.merchandise.market_price,
            'despatch_type': goods.merchandise.despatch_type,
            'production_id': goods.merchandise.production.id,
            'production_name': goods.merchandise.production.name,
            'school_id': goods.years.relations.school.id,
            'school_name': goods.years.relations.school.name,
            'major_id':goods.years.relations.major.id,
            'major_name': goods.years.relations.major.name,
            'description': goods.merchandise.description,
            'years_id': goods.years.id,
            'duration':goods.years.duration,
            'category':goods.years.category,
            'use_status': goods.merchandise.use_status,
            'remark': goods.merchandise.remark,
            'specification_list':[{
                'id': specification.id,
                "show_image":specification.show_image,
                "sale_price":specification.sale_price,
                'original_price': specification.sale_price,
                "stock":specification.stock,
                "specification_value_list":[{
                    "category":specification_value.category,
                    "attribute":specification_value.attribute
                } for specification_value in specification.specification_value_list]
            } for specification in goods.merchandise.specification_list]
        }
        return response


class Search(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页面")
    request.search_info = RequestField(
        DictField,
        desc = "搜索商品",
        conf = {
            'title': CharField(desc = "标题", is_required = False),
            'province': CharField(desc = "学校所在省", is_required = False),
            'city': CharField(desc = "学校所在市", is_required = False),
            'school_id': IntField(desc = "学校id", is_required = False),
            'major_id': IntField(desc = "专业id", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "商品列表搜索接口",
        fmt = DictField(
            desc = "商品内容",
            conf = {
                'id': IntField(desc = "编号"),
                'title': CharField(desc = "标题"),
                'slideshow': ListField(
                    desc = '轮播图',
                    fmt = CharField(desc = "图片地址")
                ),
                'use_status': CharField(
                    desc = "使用状态",
                    choices = UseStatus.CHOICES
                ),
                'production_id': IntField(desc = "产品ID"),
                'production_name': CharField(desc = "产品名称"),
                'brand_id': IntField(desc = "品牌ID"),
                'brand_name': CharField(desc = "品牌名称"),
                'school_id': IntField(desc = "学校ID"),
                'school_name': CharField(desc = "学校名称"),
                'major_id': IntField(desc = "专业ID"),
                'major_name': CharField(desc = "专业名称"),
                'is_hot':BooleanField(desc = "是否热门"),
                'years_id': IntField(desc = "学年ID"),
                'duration':CharField(
                    desc = "时长",
                    choices = DurationTypes.CHOICES
                ),
                'category':CharField(
                    desc = "分类",
                    choices = CategoryTypes.CHOICES
                ),
                'create_time': DatetimeField(desc = "创建时间"),
                'specification_list': ListField(
                    desc = "规格列表",
                    fmt = DictField(
                        desc = "规格详情",
                        conf = {
                            "id": IntField(desc = "规格id"),
                            "sale_price": IntField(desc = "销售价为，单位：分"),
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
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "商品搜索"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        auth = self.auth_user
        agent = AgentServer.get(auth.agent_id)
        school_info = {}
        if 'province' in request.search_info:
            province = request.search_info.pop('province')
            school_info.update({
                'province': province
            })
        if 'city' in request.search_info:
            city = request.search_info.pop('city')
            school_info.update({
                'city': city
            })
        if len(school_info) > 0:
            school_id_list = UniversityServer.search_school_id_list(
                **school_info
            )
            request.search_info.update({
                'school_id__in': school_id_list
            })
        request.search_info.update({
            "agent_id":agent.id
        })
        spliter = GoodsServer.search_goods(
            request.current_page,
            **request.search_info
        )
        UniversityServer.hung_major(spliter.data)
        UniversityServer.hung_school(spliter.data)
        MerchandiseServer.hung_merchandise(spliter.data)
        merchandise_list = [goods.merchandise for goods in spliter.data]
        ProductionServer.hung_production(merchandise_list)
        UniversityYearsServer.hung_years(spliter.data)
        return spliter

    def fill(self, response, spliter):
        data_list = [{
            'id': goods.id,
            'title': goods.merchandise.title,
            'slideshow':json.loads(goods.merchandise.slideshow),
            'use_status': goods.merchandise.use_status,
            'production_id': goods.merchandise.production.id,
            'production_name': goods.merchandise.production.name,
            'brand_id': goods.merchandise.production.brand.id,
            'brand_name':goods.merchandise.production.brand.name,
            'school_id': goods.years.relations.school.id,
            'school_name': goods.years.relations.school.name,
            'major_id':goods.years.relations.major.id,
            'major_name': goods.years.relations.major.name,
            'is_hot':goods.is_hot,
            'years_id': goods.years.id,
            'duration':goods.years.duration,
            'category':goods.years.category,
            'create_time':goods.create_time,
            'specification_list':[{
                "id": specification.id,
                "sale_price":specification.sale_price,
                "specification_value_list":[{
                    "category":specification_value.category,
                    "attribute":specification_value.attribute
                } for specification_value in specification.specification_value_list]
            } for specification in goods.merchandise.specification_list]
        } for goods in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Add(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.goods_info = RequestField(
        DictField,
        desc = "商品详情",
        conf = {
            'title': CharField(desc = "标题"),
            'video_display': CharField(desc = "宣传视频", is_required = False),
            'slideshow': ListField(
                desc = '轮播图',
                fmt = CharField(desc = "图片地址")
            ),
            'detail': ListField(
                desc = '详情页',
                fmt = CharField(desc = "图片地址")
            ),
            'market_price': IntField(desc = "市场价, 单位:分"),
            'despatch_type': CharField(
                desc = "发货方式",
                choices = DespatchService.CHOICES
            ),
            'production_id': IntField(desc = "产品ID"),
            'years_id': IntField(desc = "学年id"),
            'description':CharField(desc = "商品描述"),
            'remark': CharField(desc = "备注", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.goods_id = ResponseField(IntField, desc = "商品ID")

    @classmethod
    def get_desc(cls):
        return "商品添加接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        auth = self.auth_user
        agent = AgentServer.get(auth.agent_id)
        year = UniversityYearsServer.get(
            request.goods_info.pop('years_id')
        )
        production = ProductionServer.get(
            request.goods_info.pop('production_id')
        )
        merchandise_info = {
            "title":request.goods_info.pop('title'),
            "company_id":agent.company_id,
            "slideshow":json.dumps(request.goods_info.pop('slideshow')),
            "video_display":request.goods_info.pop('video_display', ''),
            "detail":json.dumps(request.goods_info.pop('detail')),
            "market_price":request.goods_info.pop('market_price'),
            "despatch_type":request.goods_info.pop('despatch_type'),
            "production_id":production.id,
            "remark":request.goods_info.pop('remark', ''),
            'description':request.goods_info.pop('description'),
            "pay_types":"[]",
            "pay_services":"[]",
        }
        merchandise = MerchandiseServer.generate(**merchandise_info)

        goods_info = {
            "school_id":year.relations.school_id,
            "major_id":year.relations.major_id,
            "merchandise_id":merchandise.id,
            "agent_id":agent.id,
            "relations_id":year.relations_id,
            "years_id":year.id,
        }
        goods = GoodsServer.create_goods(**goods_info)
        return goods

    def fill(self, response, goods):
        response.goods_id = goods.id
        return response


class Update(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")
    request.goods_info = RequestField(
        DictField,
        desc = "商品详情",
        conf = {
            'title': CharField(desc = "标题"),
            'video_display': CharField(desc = "宣传视频", is_required = False),
            'slideshow': ListField(
                desc = '轮播图',
                fmt = CharField(desc = "图片地址")
            ),
            'detail': ListField(
                desc = '详情页',
                fmt = CharField(desc = "图片地址")
            ),
            'market_price': IntField(desc = "市场价, 单位:分"),
            'despatch_type': CharField(
                desc = "发货方式",
                choices = DespatchService.CHOICES
            ),
            'years_id': IntField(desc = "学年ID"),
            "description":CharField(desc = "商品描述"),
            'remark': CharField(desc = "备注", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "商品信息更新接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        merchandise = MerchandiseServer.get(goods.merchandise_id)
        if merchandise.use_status == UseStatus.ENABLE:
            raise BusinessError("请先下架此商品")
        year = UniversityYearsServer.get(
            request.goods_info.pop('years_id')
        )
        goods_update_info = {
            "school_id":year.relations.school_id,
            "major_id":year.relations.major_id,
            "relations_id":year.relations_id,
            "years_id":year.id,
        }
        GoodsServer.update_goods(goods, **goods_update_info)
        merchandise_update_info = {
            "title":request.goods_info.pop('title'),
            "slideshow":json.dumps(request.goods_info.pop('slideshow')),
            "video_display":request.goods_info.pop('video_display', ''),
            "detail":json.dumps(request.goods_info.pop('detail')),
            "market_price":request.goods_info.pop('market_price'),
            "despatch_type":request.goods_info.pop('despatch_type'),
            "remark":request.goods_info.pop('remark', ''),
            "description":request.goods_info.pop('description'),
        }
        MerchandiseServer.update(goods.merchandise_id,
                                 **merchandise_update_info)

    def fill(self, response):
        return response


class Setuse(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "商品上下架接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        merchandise = MerchandiseServer.get(goods.merchandise_id)
        use_status = UseStatus.ENABLE
        if merchandise.use_status == UseStatus.ENABLE:
            use_status = UseStatus.FORBIDDENT
        else:
            raise BusinessError("暂无权限上架商品")
        merchandise.update(use_status = use_status)

    def fill(self, response):
        return response


class Remove(AgentStaffAuthorizedApi):
    """删除商品信息"""
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "商品信息删除接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        merchandise = MerchandiseServer.get(goods.merchandise_id)
        if merchandise.use_status == UseStatus.ENABLE:
            raise BusinessError("请先下架此商品")
        if OrderItemServer.search_all(goods_id = goods.id).count() > 0:
            raise BusinessError("存在订单无法删除")
        MerchandiseServer.remove(merchandise.id)
        goods.delete()

    def fill(self, response):
        return response


class SearchAll(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "产品列表",
        fmt = DictField(
            desc = "产品信息",
            conf = {
                'id': IntField(desc = '产品id'),
                'name': CharField(desc = "产品名称"),
                'children': ListField(
                    desc = "商品列表",
                    fmt = DictField(
                        desc = "商品信息",
                        conf = {
                            'id':IntField(desc = '学校id'),
                            'name':CharField(desc = '学校名称'),
                            'children':ListField(
                                desc = '专业列表',
                                fmt = DictField(
                                    desc = '专业信息',
                                    conf = {
                                        'id':IntField(desc = '专业id'),
                                        'name':CharField(desc = '专业名称'),
                                        'children':ListField(
                                            desc = '商品列表',
                                            fmt = DictField(
                                                desc = '商品信息',
                                                conf = {
                                                    'id': IntField(desc = "商品id"),
                                                    'name': CharField(desc = "商品名称"),
                                                    'specification_list': ListField(
                                                        desc = "规格列表",
                                                        fmt = DictField(
                                                            desc = "规格详情",
                                                            conf = {
                                                                "id": IntField(desc = "规格id"),
                                                                "show_image": CharField(desc = "展示图片"),
                                                                "sale_price": IntField(desc = "销售价为，单位：分"),
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
                                                }
                                            )
                                        )
                                    }
                                )
                            )
                        }
                    )
                )
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "产品商品搜索"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        goods_list = list(GoodsServer.search_all_goods(
            use_status = UseStatus.ENABLE,
            agent_id = self.auth_user.agent_id
        ))
        MerchandiseServer.hung_merchandise(goods_list)
        ProductionServer.hung_production([goods.merchandise for goods in goods_list])
        UniversityServer.hung_school(goods_list)
        UniversityServer.hung_major(goods_list)
        return goods_list

    def fill(self, response, goods_list):
        mapping = {}
        for goods in goods_list:
            production = goods.merchandise.production
            school = goods.school
            major = goods.major
            if production.id not in mapping:
                mapping[production.id] = {
                    "id":production.id,
                    "name":production.name,
                    "school_ids":[],
                    "children":{}
                }
            if school.id not in mapping[production.id]["school_ids"]:
                mapping[production.id]["school_ids"].append(school.id)
                mapping[production.id]["children"][school.id] = {
                    "id":school.id,
                    "name":school.name,
                    "major_ids":[],
                    "children":{}
                }
            if major.id not in mapping[production.id]["children"][school.id]["major_ids"]:
                mapping[production.id]["children"][school.id]["major_ids"].append(major.id)
                mapping[production.id]["children"][school.id]["children"][major.id] = {
                    "id":major.id,
                    "name":major.name,
                    "children":[]
                }
            mapping[production.id]["children"][school.id]["children"][major.id]["children"].append(goods)

        data_list = []
        for k, v in mapping.items():
            product_children = []
            for s_id, school in v["children"].items():
                school_children = []
                for m_id, major in school["children"].items():
                    major_children = []
                    for goods in major["children"]:
                        specification_list = [{
                            "id": specification.id,
                            'show_image': specification.show_image,
                            "sale_price": specification.sale_price,
                            "specification_value_list": [{
                                "category": specification_value.category,
                                "attribute": specification_value.attribute
                            } for specification_value in specification.specification_value_list]
                        } for specification in goods.merchandise.specification_list]
                        goods_dic = {
                            "id":goods.id,
                            "name":goods.merchandise.title,
                            "specification_list":specification_list,
                        }
                        major_children.append(goods_dic)
                    major_dic = {
                       "id":major["id"],
                       "name":major["name"],
                       "children":major_children,
                    }
                    school_children.append(major_dic)
                school_dic = {
                   "id":school["id"],
                   "name":school["name"],
                   "children":school_children,
                }
                product_children.append(school_dic)
            product_dic = {
                "id":v["id"],
                "name":v["name"],
                "children":product_children,
            }
            data_list.append(product_dic)
        response.data_list = data_list
        return response

    '''
    def fill(self, response, goods_list):
        mapping = {}
        for goods in goods_list:
            production = goods.merchandise.production
            if production.id not in mapping:
                production.goods_list = [goods]
                mapping.update({
                    production.id: production
                })
            else:
                production = mapping.get(production.id)
                production.goods_list.append(goods)
        data_list = []
        for production in mapping.values():
            data_list.append({
                'id': production.id,
                'name': production.name,
                'children': [{
                    'id': goods.id,
                    'name': goods.merchandise.title,
                    'major_name': goods.major.name,
                    'specification_list': [{
                        "id": specification.id,
                        'show_image': specification.show_image,
                        "sale_price": specification.sale_price,
                        "specification_value_list": [{
                            "category": specification_value.category,
                            "attribute": specification_value.attribute
                        } for specification_value in specification.specification_value_list]
                    } for specification in goods.merchandise.specification_list]
                } for goods in production.goods_list]
            })
        response.data_list = data_list
        return response
    '''

class Share(AgentStaffAuthorizedApi):
    """商品信息分享"""
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")

    response = with_metaclass(ResponseFieldSet)
    response.url = ResponseField(CharField, desc = "分享连接")

    @classmethod
    def get_desc(cls):
        return "商品信息分享接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        merchandise = MerchandiseServer.get(goods.merchandise_id)
        if merchandise.use_status == UseStatus.FORBIDDENT:
            raise BusinessError("下架商品无法生成连接")

        url = "type=goods&goods_id={goods_id}".format(
            goods_id = goods.id
        )
        return url

    def fill(self, response, url):
        response.url = url
        return response
