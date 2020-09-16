# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.dictwrapper import DictWrapper
from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.contract.utils.constant import TemplateStatus
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.services.agent.contract.manager import TemplateServer, \
     TemplateParamServer
from abs.services.crm.contract.manager import ParamServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.agent.order.manager import OrderItemServer


class Add(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.template_info = RequestField(
        DictField,
        desc = "模板详情",
        conf = {
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
            'status': CharField(desc = "合同模板状态(draft:草稿,wait:待审核)"),
            'template_param_list':ListField(
                desc = "合同参数列表",
                fmt = DictField(
                    desc = "合同参数内容",
                    conf = {
                        'param_id': IntField(desc = "参数id"),
                        'page_number': IntField(desc = "参数所属页码"),
                        'coordinate_x':CharField(desc = "参数位置x坐标"),
                        'coordinate_y': CharField(desc = "参数位置y坐标"),
                        'width': CharField(desc = "参数宽度", is_required = False),
                        'height': CharField(desc = "参数高度", is_required = False),
                    }
                )
            )
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.template_id = ResponseField(IntField, desc = "合同模板id")

    @classmethod
    def get_desc(cls):
        return "合同模板添加接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        if request.template_info["status"] not in \
        (TemplateStatus.DRAFT, TemplateStatus.WAIT):
            raise BusinessError("合同状态异常，禁止添加")
        agent = self.auth_agent
        request.template_info["background_img_url"] = \
            json.dumps(request.template_info["background_img_url"])
        request.template_info.update({"agent_id":agent.id})
        template = TemplateServer.create(**request.template_info)

        template_param_list = []
        for template_param in request.template_info["template_param_list"]:
            template_param_list.append(DictWrapper(template_param))
        ParamServer.huang_param(template_param_list)
        TemplateParamServer.batch_create(template, template_param_list)
        return template

    def fill(self, response, template):
        response.template_id = template.id
        return response


class Search(AgentStaffAuthorizedApi):
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
        agent = self.auth_agent
        request.search_info.update({
            "agent_id":agent.id
        })
        template_spliter = TemplateServer.search(
             request.current_page,
             **request.search_info
        )
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
               'create_time': template.create_time,
          }  for template in template_spliter.data]
        response.data_list = data_list
        response.total = template_spliter.total
        response.total_page = template_spliter.total_page
        return response


class SearchAll(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "合同参数列表",
        fmt = DictField(
            desc = "合同参数内容",
            conf = {
               'id': IntField(desc = "合同模板id"),
               'name': CharField(desc = "合同模板名称"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "所有合同模板搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = self.auth_agent
        search_info = {
            "agent_id":agent.id,
            "status":TemplateStatus.ADOPT
        }
        template_list = TemplateServer.search_all(
             **search_info
        )
        return template_list

    def fill(self, response, template_list):
        data_list = [{
               'id': template.id,
               'name': template.name,
          }  for template in template_list]
        response.data_list = data_list
        return response


class Get(AgentStaffAuthorizedApi):
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


class Update(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.template_id = RequestField(IntField, desc = "合同模板id")
    request.template_info = RequestField(
        DictField,
        desc = "合同模板信息",
        conf = {
           'name': CharField(desc = "合同模板名称", is_required = False),
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
            'status': CharField(
                desc = "合同模板名称(draft:草稿,wait:待审核)",
                is_required = False
            ),
            'template_param_list':ListField(
                desc = "合同参数列表",
                fmt = DictField(
                    desc = "合同参数内容",
                    conf = {
                        'param_id': IntField(desc = "参数id"),
                        'page_number': IntField(desc = "参数所属页码"),
                        'coordinate_x':CharField(desc = "参数位置x坐标"),
                        'coordinate_y': CharField(desc = "参数位置y坐标"),
                        'width': CharField(desc = "参数宽度", is_required = False),
                        'height': CharField(desc = "参数高度", is_required = False),
                    }
                )
            )
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "合同模板编辑接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        template = TemplateServer.get(request.template_id)
        if template.status in (TemplateStatus.WAIT, TemplateStatus.ADOPT):
            raise BusinessError("此合同状态禁止编辑")
        if request.template_info["status"] not in \
        (TemplateStatus.DRAFT, TemplateStatus.WAIT):
            raise BusinessError("合同状态异常，禁止添加")
        param_list = request.template_info.pop("template_param_list")
        if "background_img_url" in request.template_info:
            request.template_info["background_img_url"] = \
                json.dumps(request.template_info["background_img_url"])
        template = TemplateServer.update(
            template,
            **request.template_info
        )

        template_param_list = []
        for template_param in param_list:
            template_param_list.append(DictWrapper(template_param))
        ParamServer.huang_param(template_param_list)
        TemplateParamServer.batch_create(template, template_param_list)

    def fill(self, response):
        return response


class Remove(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.template_id = RequestField(IntField, desc = "合同模板id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "合同模板删除接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        template = TemplateServer.get(request.template_id)
        goods_qs = GoodsServer.search_all_goods(
            template_id = template.id
        )
        if goods_qs.count() > 0:
            raise BusinessError("存在商品禁止删除")
        order_item_qs = OrderItemServer.search_all(
            template_id = template.id,
            order__status__in = (OrderStatus.ORDER_LAUNCHED, \
                                 OrderStatus.PAYMENT_FINISHED)
        )
        if order_item_qs.count() > 0:
            raise BusinessError("存在此合同交易中得订单禁止删除")
        TemplateServer.remove(template)

    def fill(self, response):
        return response


class Submit(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.template_id = RequestField(IntField, desc = "合同模板id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "合同模板提交审核接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        template = TemplateServer.get(
            request.template_id,
        )
        if template.status != TemplateStatus.DRAFT:
            raise BusinessError("此合同模板状态不允许提交")
        template.update(status = TemplateStatus.WAIT)

    def fill(self, response):
        return response
