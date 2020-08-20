# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.event.utils.constant import TrackTypes
from abs.services.agent.customer.manager import AgentCustomerServer, \
     SaleChanceServer
from abs.services.agent.event.manager import TrackEventServer
from abs.services.agent.staff.manager import AgentStaffServer


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
                'organization_name': CharField(desc = "部门名称"),
                'track_type': CharField(
                    desc = "拜访方式",
                    choices = TrackTypes.CHOICES
                ),
                'describe': CharField(desc = "拜访结果"),
                'remark': CharField(desc = "备注"),
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
        spliter = TrackEventServer.search(
            request.current_page,
            **search_info
        )
        AgentStaffServer.hung_staff(spliter.data)
        return spliter

    def fill(self, response, spliter):
        data_list = [{
                'id': track.id,
                'staff_name': track.staff.name,
                'organization_name': '公司',
                'track_type': track.track_type,
                'describe': track.describe,
                'remark': track.remark,
                'create_time': track.create_time,
              } for track in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Add(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.agent_customer_id = RequestField(IntField, desc = "客户id")
    request.track_info = RequestField(
        DictField,
        desc = "跟踪信息",
        conf = {
            'track_type': CharField(
                desc = "拜访方式",
                choices = TrackTypes.CHOICES
            ),
            'describe': CharField(desc = "拜访结果"),
            'remark': CharField(desc = "备注", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.track_id = ResponseField(IntField, desc = "跟踪记录id")

    @classmethod
    def get_desc(cls):
        return "添加跟踪记录接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        auth = self.auth_user
        agent_customer = AgentCustomerServer.get(
            request.agent_customer_id
        )
        request.track_info.update({
            "staff_id":auth.id,
            "organization_id":0,
            "agent_customer_id":agent_customer.id,
            "agent_id":auth.agent_id,
        })
        track = TrackEventServer.create(
            **request.track_info
        )
        return track

    def fill(self, response, track):
        response.track_id = track.id
        return response




