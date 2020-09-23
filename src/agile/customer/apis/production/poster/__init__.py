# coding=UTF-8
import json
import datetime
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi
from infrastructure.core.exception.business_error import BusinessError
from abs.middleground.business.transaction.utils.constant import PayService
from abs.services.agent.goods.manager import GoodsServer, PosterServer
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.services.crm.university.manager import UniversityServer, UniversityYearsServer
from abs.services.agent.agent.manager import AgentServer
from abs.middleground.business.person.manager import PersonServer


class Get(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.poster_id = RequestField(IntField, desc = "海报id")

    response = with_metaclass(ResponseFieldSet)
    response.goods_info = ResponseField(DictField, desc = "商品信息", conf = {
        'id': IntField(desc = "商品id"),
        'slideshow': ListField(desc = "轮播图", fmt = CharField(desc = "url")),
        'video_display': CharField(desc = "展示视频"),
        'detail': ListField(desc = "商品详情", fmt = CharField(desc = "url")),
        'min_price': IntField(desc = "价格"),
        'title': CharField(desc = "标题"),
        'description': CharField(desc = "描述"),
        'despatch_type': CharField(desc = "发货方式"),
        'school_city': CharField(desc = "学校城市"),
        'month_quantity': IntField(desc = "月销数量"),
        'school_name': CharField(desc = "学校名称"),
        'major_name': CharField(desc = "专业名称"),
        'duration': CharField(desc = "学年"),
        'brand_name': CharField(desc = "品牌"),
        'production_name': CharField(desc = "产品名"),
        'agent_name': CharField(desc = "代理商名称"),
        'deposit':IntField(desc = "首付金额"),
        'pay_services':CharField(
            desc = "支付类型",
            choices = PayService.CHOICES
        ),
        'specification_list': ListField(
            desc = "规格列表",
            fmt = DictField(
                desc = "规格",
                conf = {
                    'id': IntField(desc = "id"),
                    'sale_price': IntField(desc = "价格"),
                    'original_price': IntField(desc = "原价"),
                    'stock': IntField(desc = "库存"),
                    'show_image': CharField(desc = "展示图片"),
                    'specification_value_list': ListField(
                        desc = "商品规格值",
                        fmt = DictField(
                            desc = '规格值',
                            conf = {
                                'category': CharField(desc = "属性分类"),
                                'attribute': CharField(desc = "属性值")
                            }
                        )
                    )
                }
            )
        )
    })

    @classmethod
    def get_desc(cls):
        return "商品详情"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        poster = PosterServer.get(request.poster_id)
        if poster.expire_date < datetime.date.today():
            raise BusinessError('海报已过期')
        person = PersonServer.get(self.auth_user.person_id)
        if not person or person.phone != poster.phone:
            raise BusinessError('专属二维码，您无权限扫码')
        goods = poster.goods
        UniversityServer.hung_major([goods])
        UniversityServer.hung_school([goods])
        MerchandiseServer.hung_merchandise([goods])
        ProductionServer.hung_production([goods.merchandise])
        UniversityYearsServer.hung_years([goods])
        AgentServer.hung_agent([goods])
        return poster

    def fill(self, response, poster):
        goods = poster.goods
        response.goods_info = {
            'id': goods.id,
            'slideshow': json.loads(goods.merchandise.slideshow),
            'video_display': goods.merchandise.video_display,
            'detail': json.loads(goods.merchandise.detail),
            'min_price': min([
                specification.sale_price
                for specification in goods.merchandise.specification_list
            ]) if goods.merchandise.specification_list else 0,
            'title': goods.merchandise.title,
            'description': goods.merchandise.description,
            'despatch_type': goods.merchandise.despatch_type,
            'school_city': goods.school.city,
            'month_quantity': 0,
            'school_name': goods.school.name,
            'major_name': goods.major.name,
            'duration': goods.years.get_duration_display(),
            'brand_name': goods.merchandise.production.brand.name,
            'production_name': goods.merchandise.production.name,
            'agent_name': goods.agent.name,
            'deposit':poster.deposit,
            'pay_services':poster.pay_services,
            'specification_list': [{
                'id': poster_specification.specification.id,
                'original_price': poster_specification.original_price,
                'sale_price': poster_specification.sale_price,
                'stock': poster_specification.specification.stock,
                'show_image': poster_specification.specification.show_image,
                'specification_value_list': [{
                    'category': value.category,
                    'attribute': value.attribute
                } for value in poster_specification.specification.specification_value_list]
            } for poster_specification in poster.poster_specification_list]
        }
        return response
