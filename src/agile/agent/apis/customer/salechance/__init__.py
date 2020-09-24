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
from abs.services.agent.event.utils.constant import OperationTypes
from abs.services.agent.customer.manager import AgentCustomerServer, \
     SaleChanceServer
from abs.services.agent.agent.manager import AgentStaffServer
from abs.services.crm.production.manager import ProductionServer
from abs.services.agent.event.manager import OperationEventServer


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
                'agent_customer_id': IntField(desc = "客户id"),
                'phone': CharField(desc = "客户手机号"),
                'name': CharField(desc = "客户姓名"),
                'wechat': CharField(desc = "客户微信号"),
                'education': CharField(desc = "学历"),
                'intention': CharField(desc = "客户意向"),
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
            permission = AgentStaffServer.get_permission(
                auth
            )
            request.search_info.update({
                "staff_id__in":permission.data[0]
            })
        request.search_info.update({
            "agent_id":auth.company_id
        })
        spliter = SaleChanceServer.search(
            request.current_page,
            **request.search_info
        )
        AgentStaffServer.hung_staff(spliter.data)
        ProductionServer.hung_production(spliter.data)
        agent_customer_list = [obj.agent_customer for obj in spliter.data]
        return spliter

    def fill(self, response, spliter):
        data_list = [{
                'id': sale_chance.id,
                'agent_customer_id': sale_chance.agent_customer.id,
                'phone': sale_chance.agent_customer.phone,
                'name':sale_chance.agent_customer.name,
                'wechat':sale_chance.agent_customer.wechat,
                'education': sale_chance.agent_customer.education,
                'intention': sale_chance.intention,
                'production_id': sale_chance.production.id if \
                                 sale_chance.production else "",
                'production_name': sale_chance.production.name if \
                                   sale_chance.production else "",
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
            'gender': CharField(desc = "客户性别", is_required = False),
            'phone': CharField(desc = "客户手机号码"),
            'production_id': IntField(desc = "产品id"),
            'city': CharField(desc = "省市区", is_required = False),
            'education': CharField(desc = "学历", is_required = False),
            'source': CharField(desc = "客户来源", is_required = False),
            'wechat': CharField(desc = "微信", is_required = False),
            'qq': CharField(desc = "QQ号码", is_required = False),
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
        agent = auth.company
        production_id = request.sale_chance_info.pop("production_id")
        production = ProductionServer.get(production_id)
        customer = AgentCustomerServer.check_byphone(
            request.sale_chance_info["phone"],
            agent.id
        )
        remark = request.sale_chance_info.pop("remark") if \
               "remark" in request.sale_chance_info else ""
        customer_info = request.sale_chance_info
        customer_info.update({
            "agent_id":agent.id,
            "person_id":0,
        })
        if customer is None:
            customer = AgentCustomerServer.create(
                **customer_info
            )
        else:
            customer.update(**customer_info)
            if SaleChanceServer.is_exist(customer):
                raise BusinessError("此客户机会已存在")
        sale_chance_info = {
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
             ),
             "remark":remark
        }
        SaleChanceServer.create(**sale_chance_info)

    def fill(self, response):
        return response


class Get(AgentStaffAuthorizedApi):
    """
        获取机会
    """
    request = with_metaclass(RequestFieldSet)
    request.sale_chance_id = RequestField(IntField, desc = "机会id")

    response = with_metaclass(ResponseFieldSet)
    response.sale_chance_info = ResponseField(
        DictField,
        desc = "机会详情",
        conf = {
            'id': IntField(desc = "机会id"),
            'agent_customer_id': IntField(desc = "代理商客户id"),
            'name': CharField(desc = "客户姓名"),
            'gender': CharField(desc = "客户性别"),
            'phone': CharField(desc = "客户手机号码"),
            'production_id': IntField(desc = "偏好产品id"),
            'production_name': CharField(desc = "偏好产品"),
            'city': CharField(desc = "省市区"),
            'education': CharField(desc = "学历"),
            'source': CharField(desc = "客户来源"),
            'wechat': CharField(desc = "微信"),
            'qq': CharField(desc = "QQ号码"),
            'intention': DateField(desc = "意向"),
            'end_time': DateField(desc = "备注"),
            'create_time': DatetimeField(desc = "备注"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "机会详情接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        sale_chance = SaleChanceServer.get(request.sale_chance_id)
        ProductionServer.hung_production([sale_chance])
        return sale_chance


    def fill(self, response, sale_chance):
        response.sale_chance_info = {
            'id': sale_chance.id,
            'agent_customer_id': sale_chance.agent_customer.id,
            'name': sale_chance.agent_customer.name,
            'gender': sale_chance.agent_customer.gender,
            'phone':sale_chance.agent_customer.phone,
            'production_id': sale_chance.production.id if \
                             sale_chance.production else "",
            'production_name': sale_chance.production.name if \
                               sale_chance.production else "",
            'city': sale_chance.agent_customer.city,
            'education': sale_chance.agent_customer.education,
            'source':sale_chance.agent_customer.source,
            'wechat':sale_chance.agent_customer.wechat,
            'qq':sale_chance.agent_customer.qq,
            'intention': sale_chance.intention,
            'end_time':sale_chance.end_time,
            'create_time': sale_chance.create_time,
        }
        return response


class End(AgentStaffAuthorizedApi):
    """
        结束机会
    """
    request = with_metaclass(RequestFieldSet)
    request.sale_chance_id = RequestField(IntField, desc = "机会id")

    response = with_metaclass(ResponseFieldSet)


    @classmethod
    def get_desc(cls):
        return "机会结束接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        sale_chance = SaleChanceServer.end(request.sale_chance_id)


    def fill(self, response):
        return response


class Update(AgentStaffAuthorizedApi):
    """
    修改机会
    """
    request = with_metaclass(RequestFieldSet)
    request.sale_chance_id = RequestField(IntField, desc = "机会id")
    request.update_info = RequestField(
        DictField,
        desc = "机会详情",
        conf = {
            'intention': CharField(desc = "客户意向", \
                                   is_required = False),
            'production_id': IntField(desc = "偏好产品id", \
                                      is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "机会修改接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        sale_chance = SaleChanceServer.get(request.sale_chance_id)
        o_intention_name = sale_chance.get_intention_display()
        o_production = ProductionServer.get(sale_chance.production_id)
        sale_chance = SaleChanceServer.update(
            sale_chance,
            **request.update_info
        )
        n_intention_name = sale_chance.get_intention_display()
        n_production = ProductionServer.get(sale_chance.production_id)
        describe = ""
        if o_intention_name != n_intention_name:
            describe = "{d}客户意向由{o}变更为{n};".format(
                d = describe,
                o = o_intention_name,
                n = n_intention_name
            )
        if o_production != n_production:
            describe = "{d}客户偏好由{o}变更为{n}".format(
                d = describe,
                o = o_production.name if o_production else "无",
                n = n_production.name,
            )
        if describe:
            auth = self.auth_user
            OperationEventServer.create(**{
                "staff_id":auth.id,
                "organization_id":0,
                "agent_customer_id":sale_chance.agent_customer.id,
                "agent_id":auth.company_id,
                "type":OperationTypes.INTENTION,
                "describe":describe
            })


    def fill(self, response):
        return response
