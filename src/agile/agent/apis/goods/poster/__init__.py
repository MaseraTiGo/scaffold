# coding=UTF-8
import json
import datetime
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField, DateField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.goods.manager import PosterServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.agent.customer.manager import SaleChanceServer
from abs.services.crm.university.manager import UniversityServer
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.merchandise.manager import MerchandiseServer


class Add(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.poster_info = RequestField(
        DictField,
        desc = "商品详情",
        conf = {
            'sale_chance_id': IntField(desc = '机会id'),
            'goods_id': IntField(desc = "商品id"),
            'remark': CharField(desc = "备注", is_required = False),
            'pay_services': CharField(desc = "支付类型"),
            'deposit': IntField(desc = "首付款金额"),
            'specification_list': ListField(
                desc = "规格列表",
                fmt = DictField(
                    desc = "规格信息",
                    conf = {
                        'id': IntField(desc = "规格id"),
                        'sale_price': IntField(desc = "折后价"),
                        'original_price': IntField(desc = "原价")
                    }
                )
            ),
            'pay_plan': ListField(
                desc = "回款计划",
                fmt = DictField(
                    desc = "规格信息",
                    conf = {
                        'plan_amount': IntField(desc = "金额"),
                        'plan_time': CharField(desc = "时间")
                    }
                )
            )
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.poster_info = ResponseField(
        DictField,
        desc = "海报详情",
        conf = {
            'id':IntField(desc = '海报id'),
            'product_name':CharField(desc = '产品名称'),
            'school_name':CharField(desc = '学校名称'),
            'major_name':CharField(desc = '专业名称'),
            'url':CharField(desc = '海报二维码连接'),
        }
    )

    @classmethod
    def get_desc(cls):
        return "海报添加接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        if len(request.poster_info["specification_list"]) > 1:
            raise BusinessError('海报的规格只能选择一个')
        sale_chance = SaleChanceServer.get(
            request.poster_info.pop('sale_chance_id')
        )
        if self.auth_user.id != sale_chance.staff_id:
            raise BusinessError('只能生成自己客户的海报')
        if sale_chance.end_time <= datetime.date.today():
            raise BusinessError('机会已过期')
        goods = GoodsServer.get_goods(request.poster_info.pop('goods_id'))
        specification_list = request.poster_info.pop('specification_list')
        request.poster_info["pay_plan"] = json.dumps(
            request.poster_info["pay_plan"]
        )
        poster = PosterServer.add(
            specification_list,
            goods = goods,
            phone = sale_chance.agent_customer.phone,
            staff_id = self.auth_user.id,
            **request.poster_info
        )
        UniversityServer.hung_school([poster.goods])
        UniversityServer.hung_major([poster.goods])
        MerchandiseServer.hung_merchandise([poster.goods])
        ProductionServer.hung_production([poster.goods.merchandise])
        return poster

    def fill(self, response, poster):
        response.poster_info = {
            "id":poster.id,
            "product_name":poster.goods.merchandise.production.name,
            "school_name":poster.goods.school.name,
            "major_name":poster.goods.major.name,
            "url":"type=poster&poster_id={poster_id}".format(
                poster_id = poster.id
            )
        }
        return response
