# coding=UTF-8
from abs.services.crm.tool.manager.notice import NoticeServer
from agile.agent.manager.api import AgentStaffAuthorizedApi
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.field.base import CharField, DictField, \
    IntField, ListField, DatetimeField


class SearchAll(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField, desc="通知列表",
        fmt=DictField(desc="通知详情",
                      conf={
                          'title': CharField(desc="标题"),
                          'content': CharField(desc="内容"),
                          'create_time': DatetimeField(desc="通知时间")
                      }))

    @classmethod
    def get_desc(cls):
        return "获取通知"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        request.search_info = {'platform': 'agent', 'status': 'enable'}
        notice_qs_split = NoticeServer.search_all(**request.search_info)
        return notice_qs_split

    def fill(self, response, notice_qs_split):
        response.data_list = [
            {
                'title': item.title,
                'content': item.content,
                'create_time': item.create_time
            }
            for item in notice_qs_split
        ]
        return response
