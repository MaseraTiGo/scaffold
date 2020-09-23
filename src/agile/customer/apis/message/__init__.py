# coding=UTF-8
from agile.customer.manager.api import CustomerAuthorizedApi
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.field.base import CharField, DictField, \
    IntField, ListField, DatetimeField
from abs.services.customer.personal.manager.message import CustomerMessageServer


class Search(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc="当前页码"
    )
    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField, desc="消息列表",
        fmt=DictField(desc="消息详情",
                      conf={
                          'title': CharField(desc="标题"),
                          'content': CharField(desc="内容"),
                          'datetime': DatetimeField(desc="消息时间")
                      }))

    @classmethod
    def get_desc(cls):
        return "获取消息"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        customer = self.auth_user
        search_info = {'person': customer}
        notice_qs_split = CustomerMessageServer.search(request.current_page, **search_info)
        return notice_qs_split

    def fill(self, response, notice_qs_split):
        response.data_list = [
            {
                'title': item.title,
                'content': item.content,
                'datetime': item.datetime
            }
            for item in notice_qs_split.data
        ]
        response.total = notice_qs_split.total
        response.total_page = notice_qs_split.total_page
        return response


class ChangeStatus(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.message_id = RequestField(
        IntField,
        desc="消息id"
    )
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "更改消息状态接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        update_info = {'status': 'read'}
        CustomerMessageServer.update(request.message_id, **update_info)

    def fill(self, response):
        return response
