# coding=UTF-8
from abs.services.crm.tool.manager.notice import NoticeServer
from agile.wechat.manager.api import WechatAuthorizedApi
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.field.base import CharField, DictField, \
    IntField, ListField, DatetimeField


class Search(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc="当前页码"
    )
    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField, desc="通知（公告）列表",
        fmt=DictField(desc="通知（公告）详情",
                      conf={
                          'title': CharField(desc="标题"),
                          'content': CharField(desc="内容"),
                          'create_time': DatetimeField(desc="通知时间")
                      }))

    @classmethod
    def get_desc(cls):
        return "获取通知（公告）"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        request.search_info = {'platform': 'customer_wechat', 'status': 'enable'}
        notice_qs_split = NoticeServer.search(request.current_page, **request.search_info)
        return notice_qs_split

    def fill(self, response, notice_qs_split):
        response.data_list = [
            {
                'title': item.title,
                'content': item.content,
                'create_time': item.create_time
            }
            for item in notice_qs_split.data
        ]
        response.total = notice_qs_split.total
        response.total_page = notice_qs_split.total_page
        return response
