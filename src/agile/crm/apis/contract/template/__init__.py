# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.agent.contract.utils.constant import TemplateStatus
from abs.services.agent.contract.manager import TemplateServer, \
     TemplateParamServer
from abs.services.crm.agent.manager import AgentServer


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页面")
    request.search_info = RequestField(
        DictField,
        desc = "搜索合同参数",
        conf = {
              'name': CharField(desc = "合同模板名称", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "合同参数列表",
        fmt = DictField(
            desc = "合同参数内容",
            conf = {
               'id': IntField(desc = "合同模板id"),
               'name': CharField(desc = "合同模板名称"),
               'background_img_url':ListField(
                    desc = '合同模板图片',
                    fmt = DictField(
                        desc = "背景图详情",
                        conf = {
                            'page_number': IntField(desc = "背景图编号"),
                            'path_url': CharField(desc = "背景图地址"),
                            'width': IntField(desc = "背景图宽度"),
                            'height': IntField(desc = "背景图高度"),
                        }
                    )
                ),
               'status':CharField(
                    desc = "状态",
                    choices = TemplateStatus.CHOICES
                ),
               'agent_id': IntField(desc = "代理商id"),
               'agent_name': CharField(desc = "代理商名称"),
               'create_time': DatetimeField(desc = "创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "合同模板搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        request.search_info.update({
            "status__in":(TemplateStatus.WAIT, \
                          TemplateStatus.ADOPT, \
                          TemplateStatus.REFUSE)
        })
        template_spliter = TemplateServer.search(
             request.current_page,
             **request.search_info
        )
        AgentServer.hung_agent(template_spliter.data)
        return template_spliter

    def fill(self, response, template_spliter):
        data_list = [{
               'id': template.id,
               'name': template.name,
               'background_img_url':[{
                    'page_number': obj['page_number'],
                    'path_url':obj['path_url'],
                    'width': obj['width'],
                    'height':obj['height'],
                } for obj in json.loads(template.background_img_url)],
               'status':template.status,
               'agent_id':template.agent.id,
               'agent_name':template.agent.name,
               'create_time': template.create_time,
          }  for template in template_spliter.data]
        response.data_list = data_list
        response.total = template_spliter.total
        response.total_page = template_spliter.total_page
        return response


class Get(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.template_id = RequestField(IntField, desc = "合同模板id")

    response = with_metaclass(ResponseFieldSet)
    response.template_info = ResponseField(
        DictField,
        desc = "模板详情",
        conf = {
               'id': IntField(desc = "合同模板id"),
               'name': CharField(desc = "合同模板名称"),
               'background_img_url':ListField(
                    desc = '合同模板图片',
                    fmt = DictField(
                        desc = "背景图详情",
                        conf = {
                            'page_number': IntField(desc = "背景图编号"),
                            'path_url': CharField(desc = "背景图地址"),
                            'width': IntField(desc = "背景图宽度"),
                            'height': IntField(desc = "背景图高度"),
                        }
                    )
                ),
               'status':CharField(
                    desc = "状态",
                    choices = TemplateStatus.CHOICES
                ),
               'create_time': DatetimeField(desc = "创建时间"),
               'param_list':ListField(
                    desc = '合同模板参数',
                    fmt = DictField(
                    desc = "合同模板参数详情",
                    conf = {
                        'id': IntField(desc = "配置参数id"),
                        'default_value': CharField(desc = "参数默认值"),
                        'key_type': CharField(desc = "参数类型"),
                        'page_number': CharField(desc = "参数所属页码"),
                        'coordinate_x': CharField(desc = "横坐标位置"),
                        'coordinate_y': CharField(desc = "纵坐标位置"),
                        'width': CharField(desc = "宽度"),
                        'height': CharField(desc = "高度"),
                        'name': CharField(desc = "参数名称"),
                        'name_key': CharField(desc = "参数key值"),
                        'param_id':IntField(desc = "参数id"),
                    })
               ),
        }
    )

    @classmethod
    def get_desc(cls):
        return "合同模板详情接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        template = TemplateServer.get(
            request.template_id
        )
        TemplateParamServer.huang_for_template([template])
        return template

    def fill(self, response, template):
        response.template_info = {
            'id': template.id,
            'name':template.name,
            'background_img_url':[{
                'page_number': obj['page_number'],
                'path_url':obj['path_url'],
                'width': obj['width'],
                'height':obj['height'],
            } for obj in json.loads(template.background_img_url)],
            'status':template.status,
            'create_time':template.create_time,
            'param_list': [
                {
                    'id': param.id,
                    'default_value':json.loads(param.content)["default_value"],
                    'key_type':json.loads(param.content)["key_type"],
                    'page_number':param.page_number,
                    'coordinate_x':param.coordinate_x,
                    'coordinate_y': param.coordinate_y,
                    'width':param.width,
                    'height':param.height,
                    'name': json.loads(param.content)["name"],
                    'name_key':json.loads(param.content)["name_key"],
                    'param_id':param.param_id,
                }
                for param in template.param_list
            ],
        }
        return response


class Examine(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.template_id = RequestField(IntField, desc = "合同模板id")
    request.status = RequestField(CharField, desc = "合同模板状态")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "合同模板审核接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        template = TemplateServer.get(
            request.template_id,
        )
        if template.status != TemplateStatus.WAIT:
            raise BusinessError("此合同模板不允许审核")
        if request.status not in (TemplateStatus.ADOPT, TemplateStatus.REFUSE):
            raise BusinessError("审核异常")
        template.update(status = request.status)


    def fill(self, response):
        return response
