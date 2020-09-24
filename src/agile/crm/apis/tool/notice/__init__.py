# coding=UTF-8

from abs.services.crm.tool.manager.notice import NoticeServer
from abs.services.crm.tool.utils.contact import NoticeClassify, NoticePlatform, NoticeStatus
from agile.crm.manager.api import StaffAuthorizedApi
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.core.field.base import CharField, DictField, \
    IntField, ListField, DatetimeField


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页面")
    request.search_info = RequestField(
        DictField,
        desc="搜索通知（公告）记录",
        conf={
            'keywords': CharField(desc="关键字搜索", is_required=False),
            'classify': CharField(desc="类别", is_required=False, choices=NoticeClassify.CHOICES),
            'platform': CharField(desc="平台", is_required=False, choices=NoticePlatform.CHOICES),
            'status': CharField(desc="状态", is_required=False, choices=NoticeStatus.CHOICES),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="通知（公告）列表",
        fmt=DictField(
            desc="通知（公告）内容",
            conf={
                'id': IntField(desc="通知（公告）id"),
                'title': CharField(desc="标题"),
                'classify': CharField(desc="类别"),
                'content': CharField(desc="内容"),
                'status': CharField(desc="状态"),
                'platform': CharField(desc="平台"),
                'create_time': DatetimeField(desc="创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "通知（公告）搜索接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        notice_qs_split = NoticeServer.search(
            request.current_page,
            **request.search_info
        )
        return notice_qs_split

    def fill(self, response, notice_qs_split):
        data_list = [{
            'id': item.id,
            'title': item.title,
            'classify': item.classify,
            'content': item.content,
            'status': item.status,
            'platform': item.platform,
            'create_time': item.create_time
        } for item in notice_qs_split.data]
        response.data_list = data_list
        response.total = notice_qs_split.total
        response.total_page = notice_qs_split.total_page
        return response


class SearchAll(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="通知（公告）列表",
        fmt=DictField(
            desc="通知（公告）内容",
            conf={
                'id': IntField(desc="通知（公告）id"),
                'title': CharField(desc="标题"),
                'classify': CharField(desc="类别"),
                'content': CharField(desc="内容"),
                'status': CharField(desc="状态"),
                'platform': CharField(desc="平台"),
                'create_time': DatetimeField(desc="创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "启用通知（公告）搜索接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        search_info = {'platform': 'crm', 'status': 'enable'}
        notice_qs_split = NoticeServer.search_all(
            **search_info
        )
        return notice_qs_split

    def fill(self, response, notice_qs_split):
        data_list = [{
            'id': item.id,
            'classify': item.classify,
            'title': item.title,
            'content': item.content,
            'status': item.status,
            'platform': item.platform,
            'create_time': item.create_time
        } for item in notice_qs_split]
        response.data_list = data_list
        return response


class Update(StaffAuthorizedApi):
    """
    修改通知（公告）
    """
    request = with_metaclass(RequestFieldSet)
    request.notice_id = RequestField(IntField, desc="通知id")
    request.update_info = RequestField(
        DictField,
        desc="通知（公告）修改详情",
        conf={
            'title': CharField(desc="标题", is_required=False),
            'content': CharField(desc="内容", is_required=False),
            'classify': CharField(desc="名称", is_required=False, choices=NoticeClassify.CHOICES),
            'platform': CharField(desc="平台", is_required=False, choices=NoticePlatform.CHOICES),
            'status': CharField(desc="状态", is_required=False, choices=NoticeStatus.CHOICES),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改通知（公告）接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        NoticeServer.update(request.notice_id, **request.update_info)

    def fill(self, response):
        return response


class Add(StaffAuthorizedApi):
    """
    增加通知（公告）
    """
    request = with_metaclass(RequestFieldSet)
    request.notice_info = RequestField(
        DictField,
        desc="增加通知（公告）",
        conf={
            'title': CharField(desc="标题", is_required=False),
            'content': CharField(desc="内容", is_required=False),
            'classify': CharField(desc="名称", is_required=False, choices=NoticeClassify.CHOICES),
            'platform': CharField(desc="平台", is_required=False, choices=NoticePlatform.CHOICES),
            'status': CharField(desc="状态", is_required=False, choices=NoticeStatus.CHOICES),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "增加通知（公告）接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        NoticeServer.add(**request.notice_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """
    删除通知（公告）
    """
    request = with_metaclass(RequestFieldSet)
    request.notice_id = RequestField(IntField, desc="通知id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除通知（公告）接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        res_flag = NoticeServer.delete(
            request.notice_id
        )
        if not res_flag:
            raise BusinessError("删除通知异常")

    def fill(self, response):
        return response
