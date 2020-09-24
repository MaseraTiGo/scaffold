# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.event.utils.constant import OperationTypes
from abs.services.agent.customer.manager import AgentCustomerServer, \
     SaleChanceServer
from abs.services.agent.event.manager import OperationEventServer
from abs.services.agent.agent.manager import AgentStaffServer


class Search(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页面")
    request.sale_chance_id = RequestField(IntField, desc = "机会id")


    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "跟踪列表",
        fmt = DictField(
            desc = "跟踪记录",
            conf = {
                'id': IntField(desc = "记录id"),
                'staff_name': CharField(desc = "客服姓名"),
                'work_number': CharField(desc = "员工工号"),
                'operation_type': CharField(
                    desc = "操作类型",
                    choices = OperationTypes.CHOICES
                ),
                'operation_type_name': CharField(desc = "操作类型名称"),
                'describe': CharField(desc = "操作结果"),
                'create_time': DatetimeField(desc = "创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "跟踪记录添加接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        sale_chance = SaleChanceServer.get(request.sale_chance_id)
        search_info = {
            "agent_customer_id":sale_chance.agent_customer.id,
            'create_time__gte': sale_chance.create_time,
            'create_time__lte': sale_chance.end_time,
        }
        spliter = OperationEventServer.search(
            request.current_page,
            **search_info
        )
        AgentStaffServer.hung_staff(spliter.data)
        return spliter

    def fill(self, response, spliter):
        data_list = [{
                'id': operation.id,
                'staff_name': operation.staff.name,
                'work_number': operation.staff.work_number,
                'operation_type': operation.type,
                'operation_type_name': operation.get_type_display(),
                'describe': operation.describe,
                'remark': operation.remark,
                'create_time': operation.create_time,
              } for operation in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Add(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.agent_customer_id = RequestField(IntField, desc = "客户id")
    request.operation_info = RequestField(
        DictField,
        desc = "回访信息",
        conf = {
            'visit_time':DatetimeField(desc = "回访时间"),
            'describe': CharField(desc = "回访结果"),
            'remark': CharField(desc = "备注", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.operation_id = ResponseField(IntField, desc = "记录id")

    @classmethod
    def get_desc(cls):
        return "添加回访记录接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        auth = self.auth_user
        agent_customer = AgentCustomerServer.get(
            request.agent_customer_id
        )
        visit_time = request.operation_info.pop("visit_time")
        request.operation_info.update({
            "staff_id":auth.id,
            "organization_id":0,
            "agent_customer_id":agent_customer.id,
            "agent_id":auth.company_id,
            "type":OperationTypes.VISIT,
            "describe":"回访时间：{t},回访记录：{r}".format(
                t = visit_time,
                r = request.operation_info.pop("describe")
            )
        })
        operation = OperationEventServer.create(
            **request.operation_info
        )
        return operation

    def fill(self, response, operation):
        response.operation_id = operation.id
        return response




