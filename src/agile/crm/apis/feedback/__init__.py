# coding=UTF-8
import json
from agile.crm.manager.api import StaffAuthorizedApi
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.field.base import CharField, DictField, \
    IntField, ListField, DatetimeField
from abs.services.customer.personal.utils.constant import FeedType, FeedStatus
from abs.services.customer.personal.manager import FeedbackServer


class Search(StaffAuthorizedApi):
    """
    搜索意见反馈
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc="当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc="搜索意见反馈",
        conf={
            'type': CharField(desc="反馈标签", is_required=False, choices=FeedType.CHOICES),
            'status': CharField(desc="处理状态", is_required=False, choices=FeedStatus.CHOICES),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="意见反馈列表",
        fmt=DictField(
            desc="意见反馈内容",
            conf={
                'id': IntField(desc="反馈意见id"),
                'phone': CharField(desc="客户手机号"),
                'username': CharField(desc="客户姓名"),
                'type': CharField(desc="反馈标签"),
                'describe': CharField(desc="反馈描述"),
                'status': CharField(desc="处理状态"),
                'img_url': ListField(desc="图片url列表", fmt=CharField(desc="图片url")),
                'create_time': DatetimeField(desc="反馈时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "意见反馈搜索接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        feedback_qs_split = FeedbackServer.search_all(
            request.current_page,
            **request.search_info
        )
        return feedback_qs_split

    def fill(self, response, feedback_qs_split):
        data_list = [{
            'id': item.id,
            'phone': item.person.phone,
            'username': item.person.name,
            'type': item.type,
            'img_url': json.loads(item.img_url),
            'describe': item.describe,
            'status': item.status,
            'create_time': item.create_time
        } for item in feedback_qs_split.data]
        response.data_list = data_list
        response.total = feedback_qs_split.total
        response.total_page = feedback_qs_split.total_page
        return response


class UpdateStatus(StaffAuthorizedApi):
    """更新意见处理状态"""
    request = with_metaclass(RequestFieldSet)
    request.feedback_id = RequestField(
        IntField,
        desc="当前反馈ID"
    )
    request.status = RequestField(CharField, desc="意见处理状态", choices=FeedStatus.CHOICES)

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "意见反馈状态更新接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        update_info = {'status': request.status}
        FeedbackServer.update_status(
            request.feedback_id,
            **update_info
        )

    def fill(self, response):
        return response
