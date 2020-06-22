# coding=UTF-8

# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from infrastructure.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from agile.apis.base import StaffAuthorizedApi
from abs.middleware.journal import JournalMiddleware


class Search(StaffAuthorizedApi):
    """日志搜索"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页码")
    request.search_info = RequestField(DictField, desc = "日志搜索条件", conf = {
        'active_name': CharField(desc = "搜索主动方名称", is_required = False),
        'active_type': CharField(desc = "搜索主动方类型", is_required = False),
        'passive_name': CharField(desc = "搜索被动方名称", is_required = False),
        'passive_type': CharField(desc = "搜索被动方类型", is_required = False),
        'journal_type': CharField(desc = "搜索日志类型", is_required = False),
        'start_time': DateField(desc = "搜索开始时间", is_required = False),
        'end_time': DateField(desc = "搜搜结束时间", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '日志列表', fmt = DictField(desc = "日志数据", conf = {
        'id': IntField(desc = "日志id"),
        'active_name': CharField(desc = "主动方名称"),
        'active_type': CharField(desc = "主动方类型"),
        'passive_name': CharField(desc = "被动方名称"),
        'passive_type': CharField(desc = "被动方类型"),
        'journal_type': CharField(desc = "日志类型"),
        'record_detail': CharField(desc = "详情"),
        'create_time': DatetimeField(desc = "日志添加时间")
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "日志列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        if 'start_time' in request.search_info:
            start_time = request.search_info.pop('start_time')
            request.search_info['create_time__gte'] = start_time
        if 'end_time' in request.search_info:
            end_time = request.search_info.pop('end_time')
            request.search_info['create_time__lt'] = end_time
        journal_pages = JournalMiddleware.search(request.current_page, **request.search_info)

        return journal_pages

    def fill(self, response, journal_pages):
        data_list = [{
            'id': journal.id,
            'active_name': journal.active_name,
            'active_type': journal.active_type,
            'passive_name': journal.passive_name,
            'passive_type': journal.passive_type,
            'journal_type': journal.journal_type,
            'record_detail': journal.record_detail,
            'create_time': journal.create_time,
        } for journal in journal_pages.data]
        response.data_list = data_list
        response.total = journal_pages.total
        response.total_page = journal_pages.total_page
        return response
