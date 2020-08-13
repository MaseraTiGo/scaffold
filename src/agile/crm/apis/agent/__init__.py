# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.agent.manager import AgentServer
from abs.middleground.technology.permission.manager import PermissionServer
from abs.middleground.technology.permission.utils.constant import \
        PermissionTypes


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.agent_info = RequestField(
        DictField,
        desc = "代理商信息",
        conf = {
            'name': CharField(desc = "代理商名称"),
            'province': CharField(desc = "代理商省"),
            'city': CharField(desc = "代理商市"),
            'area': CharField(desc = "代理商区", is_required = False),
            'address': CharField(desc = "代理商地址"),
            'license_code': CharField(desc = "营业执照编码"),
            'license_picture': CharField(desc = "营业执照图片"),
            'official_seal': CharField(desc = "公章"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.agent_id = ResponseField(IntField, desc = "代理商ID")

    @classmethod
    def get_desc(cls):
        return "代理商添加接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = AgentServer.create(**request.agent_info)
        authorize_info = {
            'name':agent.name,
            'company_id':agent.company_id,
            'app_type':PermissionTypes.POSITION,
            'prefix':'',
            'remark':'',
        }
        platform = PermissionServer.authorize(
            **authorize_info
        )
        organization_info = {
            "parent_id":0,
            "name":"公司",
            "description":"公司",
            "remark":""
        }
        organization = PermissionServer.add_organization(
            appkey = platform.appkey,
            **organization_info
        )
        rule_group_info = {
            "name":"超级管理员权限",
            "content":"",
            "description":"超级管理员权限",
            "remark":"",
        }
        rule_group = PermissionServer.add_rule_group(
            appkey = platform.appkey,
            **rule_group_info
        )
        position_info = {
            "organization_id":organization.id,
            "rule_group_id":rule_group.id,
            "parent_id":0,
            "description":"超级管理员",
            "name":"超级管理员",
            "remark":"",
        }
        position = PermissionServer.add_position(
            appkey = platform.appkey,
            **position_info
        )
        PermissionServer.apply(platform.appkey)
        return agent

    def fill(self, response, agent):
        response.agent_id = agent.id
        return response


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页面")
    request.search_info = RequestField(
        DictField,
        desc = "搜索代理商",
        conf = {
            'name': CharField(desc = "代理商名称", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "代理商列表",
        fmt = DictField(
            desc = "代理商内容",
            conf = {
                'id': IntField(desc = "代理商id"),
                'name': CharField(desc = "代理商名称"),
                'province': CharField(desc = "省"),
                'city': CharField(desc = "市"),
                'area': CharField(desc = "区"),
                'address': CharField(desc = "详细地址"),
                'license_code': CharField(desc = "营业执照信用代码"),
                'create_time': DatetimeField(desc = "入驻时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "代理商搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        spliter = AgentServer.search(
            request.current_page,
            **request.search_info
        )
        return spliter

    def fill(self, response, spliter):
        data_list = [{
                "id":agent.id,
                "name":agent.name,
                "province":agent.province,
                "city":agent.city,
                "area":agent.area,
                "address":agent.address,
                "license_code":agent.enterprise.license_number \
                               if agent.enterprise else "",
                "create_time":agent.create_time,
              } for agent in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Get(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.agent_id = RequestField(IntField, desc = "代理商id")

    response = with_metaclass(ResponseFieldSet)
    response.agent_info = ResponseField(
        DictField,
        desc = "代理商信息",
        conf = {
            'id':IntField(desc = "代理商id"),
            'name': CharField(desc = "代理商名称"),
            'province': CharField(desc = "代理商省"),
            'city': CharField(desc = "代理商市"),
            'area': CharField(desc = "代理商区", is_required = False),
            'address': CharField(desc = "代理商地址"),
            'license_code': CharField(desc = "营业执照编码"),
            'license_picture': CharField(desc = "营业执照图片"),
            'official_seal': CharField(desc = "公章"),
            'create_time': DatetimeField(desc = "入驻时间"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "代理商查询接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = AgentServer.get(request.agent_id)
        return agent

    def fill(self, response, agent):
        agent_info = {
                "id":agent.id,
                "name":agent.name,
                "province":agent.province,
                "city":agent.city,
                "area":agent.area,
                "address":agent.address,
                "license_code":agent.enterprise.license_number,
                "license_picture":agent.enterprise.license_url,
                "official_seal":agent.official_seal,
                "create_time":agent.create_time,
          }
        response.agent_info = agent_info
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.agent_id = RequestField(IntField, desc = "代理商id")
    request.agent_info = RequestField(
        DictField,
        desc = "代理商信息",
        conf = {
            'name': CharField(desc = "代理商名称"),
            'province': CharField(desc = "代理商省"),
            'city': CharField(desc = "代理商市"),
            'area': CharField(desc = "代理商区", is_required = False),
            'address': CharField(desc = "代理商地址"),
            'license_code': CharField(desc = "营业执照编码"),
            'license_picture': CharField(desc = "营业执照图片"),
            'official_seal': CharField(desc = "公章"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "代理商更新接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = AgentServer.update(
            request.agent_id, **request.agent_info
        )

    def fill(self, response):
        return response


class SearchAll(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "代理商列表",
        fmt = DictField(
            desc = "代理商内容",
            conf = {
                'id': IntField(desc = "代理商id"),
                'name': CharField(desc = "代理商名称"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "代理商查询全部接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent_list = AgentServer.search_all()
        return agent_list

    def fill(self, response, agent_list):
        data_list = [{
                "id":agent.id,
                "name":agent.name,
              } for agent in agent_list]
        response.data_list = data_list
        return response

