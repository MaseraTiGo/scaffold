# coding=UTF-8
import datetime
import time
import random
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField, DateField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.customer.utils.constant import SourceTypes
from abs.services.agent.customer.manager import AgentCustomerServer, \
     SaleChanceServer
from abs.services.crm.agent.manager import AgentServer
from abs.services.agent.staff.manager import AgentStaffServer
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.person.manager import PersonServer


class Search(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc = "当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc = "搜索商品",
        conf = {
            'name': CharField(desc = "客户姓名", is_required = False),
            'phone': CharField(desc = "客户手机号", is_required = False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "机会列表",
        fmt = DictField(
            desc = "机会列表",
            conf = {
                'id': IntField(desc = "机会id"),
                'phone': CharField(desc = "客户手机号"),
                'name': CharField(desc = "客户姓名"),
                'wechat': CharField(desc = "客户微信号"),
                'education': CharField(desc = "学历"),
                'production_id': IntField(desc = "偏好产品id"),
                'production_name': CharField(desc = "偏好产品"),
                'city': CharField(desc = "所在城市"),
                'staff_id': IntField(desc = "员工id"),
                'staff_name': CharField(desc = "员工姓名"),
                'remark': CharField(desc = "备注"),
                'end_time': DateField(desc = "结束时间"),
                'create_time': DatetimeField(desc = "创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "机会列表接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        auth = self.auth_user
        if not auth.is_admin:
            request.search_info.update({
                "staff_id":auth.id
            })
        request.search_info.update({
            "agent_id":auth.agent_id
        })
        spliter = SaleChanceServer.search(
            request.current_page,
            **request.search_info
        )
        AgentStaffServer.hung_staff(spliter.data)
        ProductionServer.hung_production(spliter.data)
        agent_customer_list = [obj.agent_customer for obj in spliter.data]
        PersonServer.hung_persons(agent_customer_list)
        return spliter

    def fill(self, response, spliter):
        data_list = [{
                'id': sale_chance.id,
                'phone': sale_chance.agent_customer.phone,
                'name':sale_chance.agent_customer.name,
                'wechat':sale_chance.agent_customer.person.wechat if \
                         sale_chance.agent_customer.person else "",
                'education': sale_chance.agent_customer.education,
                'production_id': sale_chance.production.id,
                'production_name': sale_chance.production.name,
                'city':sale_chance.agent_customer.city,
                'staff_id': sale_chance.staff.id,
                'staff_name': sale_chance.staff.name,
                'end_time': sale_chance.end_time,
                'remark':sale_chance.remark,
                'create_time':sale_chance.create_time,
          } for sale_chance in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Add(AgentStaffAuthorizedApi):
    """
    添加机会
    """
    request = with_metaclass(RequestFieldSet)
    request.sale_chance_info = RequestField(
        DictField,
        desc = "机会详情",
        conf = {
            'name': CharField(desc = "客户姓名", is_required = False),
            'phone': CharField(desc = "客户手机号码"),
            'production_id': IntField(desc = "产品id"),
            'city': CharField(desc = "省市区", is_required = False),
            'education': CharField(desc = "学历", is_required = False),
            'remark': CharField(desc = "备注", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "机会添加接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        auth = self.auth_user
        agent = self.auth_agent
        production_id = request.sale_chance_info.pop("production_id")
        production = ProductionServer.get(production_id)
        customer = AgentCustomerServer.check_byphone(
            request.sale_chance_info["phone"],
            agent.id
        )
        if customer is None:
            customer_info = {
                "agent_id":agent.id,
                "person_id":0,
                "phone":request.sale_chance_info.pop("phone"),
                "name":request.sale_chance_info.pop("name") if \
                       "name" in request.sale_chance_info else "",
                "city":request.sale_chance_info.pop("city") if \
                       "city" in request.sale_chance_info else "",
                "education":request.sale_chance_info.pop("education")if \
                            "education" in request.sale_chance_info else "",
            }
            customer = AgentCustomerServer.create(
                **customer_info
            )
        else:
            if SaleChanceServer.is_exist(customer):
                raise BusinessError("此客户机会已存在")
        request.sale_chance_info.update({
            "agent_customer":customer,
            "agent_id":agent.id,
            "staff_id":auth.id,
            "founder_id":auth.id,
            "organization_id":0,  # 待修改
            "production_id":production.id,
            "end_time":(datetime.datetime.now() + \
                        datetime.timedelta(days = 100)).date(),
            "source":SourceTypes.CREATE,
            "batch_no":"BN{t}{r}".format(
                 t = int(time.time()),
                 r = random.randint(10000, 90000)
             )
        })
        SaleChanceServer.create(**request.sale_chance_info)

    def fill(self, response):
        return response
