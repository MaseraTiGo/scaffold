# coding=UTF-8


from django.db.models import Q

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.middleware.role import role_middleware
from abs.middleware.department import department_middleware

from model.store.model_staff import Staff, AuthAccess, AccessTypes, Role, Department

from abs.service.task.container import TaskContainerHelper
from abs.service.task.group import TaskGroupHelper


class TaskContainerServer(object):

    @classmethod
    def add(cls, **attrs):
        """添加任务容器"""
        return TaskContainerHelper.add(**attrs)

    @classmethod
    def search(cls, current_page, **search_info):
        """查询任务容器列表(分页)"""
        return TaskContainerHelper.search(current_page, **search_info)

    @classmethod
    def get(cls, task_container_id):
        """根据id查询任务容器详情"""
        return TaskContainerHelper.get(task_container_id)

    @classmethod
    def update(cls, task_container, **attrs):
        """通过id更新任务容器信息"""
        return TaskContainerHelper.update(task_container, **attrs)

    @classmethod
    def remover(cls, task_container):
        """删除任务容器信息"""
        return TaskContainerHelper.remover(task_container)


class TaskGroupServer(object):

    @classmethod
    def add(cls, **attrs):
        """添加任务组"""
        return TaskGroupHelper.add(**attrs)

    @classmethod
    def update_byid(cls, task_group_id, **attrs):
        """通过id更新任务组信息"""
        return TaskGroupHelper.update_byid(task_group_id, **attrs)

    @classmethod
    def remover_byid(cls, task_group_id):
        """通过id删除任务组信息"""
        return TaskGroupHelper.remover_byid(task_group_id)

    @classmethod
    def hung_group_bycontainer(cls, container):
        """"任务容器挂载任务组"""
        return TaskGroupHelper.hung_group_bycontainer(container)

    @classmethod
    def hung_group_bycontainerlist(cls, container_list):
        """任务容器批量挂载任务组"""
        return TaskGroupHelper.hung_group_bycontainerlist(container_list)
