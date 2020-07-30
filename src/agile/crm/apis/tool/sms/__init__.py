# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.tool.utils.contact import StatusTypes, SourceTypes, SceneTypes
from abs.services.crm.tool.manager import SmsRecordServer


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页面")
    request.search_info = RequestField(
        DictField,
        desc="搜索短信记录",
        conf={
              'phone': CharField(desc="手机号码", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="短信列表",
        fmt=DictField(
            desc="短信内容",
            conf={
                'id': IntField(desc="id"),
                'phone': CharField(desc="手机号码"),
                'content': CharField(desc="短信内容"),
                'scene': CharField(
                    desc="场景标识",
                    choices=SceneTypes.CHOICES
                ),
                'source_type':CharField(
                    desc="平台",
                    choices=SourceTypes.CHOICES
                ),
                'status': CharField(
                    desc="发送状态",
                    choices=StatusTypes.CHOICES
                ),
                'create_time': DatetimeField(desc="创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "短信列表搜索"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        sms_spliter = SmsRecordServer.search(
             request.current_page,
             **request.search_info
        )
        return sms_spliter

    def fill(self, response, sms_spliter):
        data_list = [{
                'id': sms.id,
                'phone': sms.phone,
                'content': sms.content,
                'scene': sms.scene,
                'source_type': sms.source_type,
                'status': sms.status,
                'create_time':sms.create_time,
              }  for sms in sms_spliter.data]
        response.data_list = data_list
        response.total = sms_spliter.total
        response.total_page = sms_spliter.total_page
        return response
