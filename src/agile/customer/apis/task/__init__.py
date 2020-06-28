# coding=UTF-8

'''
Created on 2018年8月17日

@author: Administrator
'''
import datetime

from infrastructure.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, \
DateField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.apis.base import StaffAuthorizedApi

from abs.middleware.journal import JournalMiddleware
from abs.middleware.task import task_middleware

from abs.service.task.manager import TaskContainerServer, TaskGroupServer


class Add(StaffAuthorizedApi):
    """添加任务"""
    request = with_metaclass(RequestFieldSet)
    request.task_container_info = RequestField(DictField, desc = "任务详情", conf = {
        'name': CharField(desc = "任务容器名称"),
        'type': CharField(desc = "任务容器类型"),
        'exec_parms': CharField(desc = "任务容器参数", is_required = False),
        'group_list': CharField(desc = "任务容器项"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "任务添加接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        TaskContainerServer.add(**request.task_container_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """任务容器搜索列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '任务容器列表', fmt = DictField(desc = "任务容器列表", conf = {
        'id':IntField(desc = "任务容器id"),
        'name': CharField(desc = "任务容器名称"),
        'type': CharField(desc = "任务容器类型"),
        'exec_parms': CharField(desc = "任务容器参数", is_required = False),
        'group_list': CharField(desc = "任务容器项"),
        'status':CharField(desc = "任务容器状态"),
        'reason': CharField(desc = "任务容器异常原因"),
        'create_time': DatetimeField(desc = "任务容器添加事件"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "任务容器列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        task_container_pages = TaskContainerServer.search(request.current_page, **request.search_info)
        return task_container_pages

    def fill(self, response, task_container_pages):
        response.data_list = [{
            'id':task_container.id,
            'name': task_container.name,
            'type':task_container.type,
            'exec_parms': task_container.exec_parms,
            'group_list':task_container.group_list,
            'status':task_container.status,
            'reason': task_container.reason,
            'create_time': task_container.create_time,
        } for task_container in task_container_pages.data]
        response.total = task_container_pages.total
        response.total_page = task_container_pages.total_page
        return response


class Remove(StaffAuthorizedApi):
    """删除任务"""
    request = with_metaclass(RequestFieldSet)
    request.task_container_id = RequestField(IntField, desc = "任务容器的id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "任务容器删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        task_container = TaskContainerServer.get(request.task_container_id)
        if task_container.status == "init" or task_container.status == "executting" or \
        task_container.status == "suspend":
            raise BusinessError("该任务容器状态禁止删除")
        TaskContainerServer.remover(task_container)

    def fill(self, response):
        return response


class UpdateStatus(StaffAuthorizedApi):
    """编辑任务状态"""
    request = with_metaclass(RequestFieldSet)
    request.task_container_id = RequestField(IntField, desc = "任务容器的id")
    request.task_container_status = RequestField(CharField, desc = "任务容器的状态")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "任务容器状态接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        task_container = TaskContainerServer.get(request.task_container_id)
        param = {"status":request.task_container_status}
        TaskContainerServer.update(task_container, **param)

        task_middleware.update_container_redis(task_container.name)

    def fill(self, response):
        return response

