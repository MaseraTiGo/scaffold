# coding=UTF-8
import datetime

from django.db.models import *

from model.store.model_task import TaskContainer, TaskGroupType, TaskGroup, GroupStatus

class TaskHelper(object):

    @classmethod
    def loading(cls):
        """初始化加载"""
        return TaskContainer.search()

    @classmethod
    def get(cls, task_container_id):
        """更新查询任务容器"""
        task_container = TaskContainer.get_byid(task_container_id)
        return task_container

    @classmethod
    def update(cls, task_container_id, task_status):
        """更新任务容器状态"""
        task_container = TaskContainer.get_byid(task_container_id)
        task_container.update(status = task_status)
        return task_container

    @classmethod
    def get_container_byname(cls, name):
        """通过任务容器名称查询任务容器"""
        task_container = None
        task_container_qs = TaskContainer.search(name = name)
        if task_container_qs.count() > 0:
            task_container = task_container_qs[0]
        return task_container

    @classmethod
    def generate_task_group(cls, **attr):
        """生成任务组"""
        task_group = TaskGroup.create(**attr)
        return task_group

    @classmethod
    def check_task_group_exist(cls, **search_info):
        """判断任务组是否已经存在"""
        task_group = None
        task_group_qs = TaskGroup.search(**search_info)
        task_group_qs = task_group_qs.filter(Q(status = GroupStatus.EXECUTTING) \
                        | Q(status = GroupStatus.SUSPEND))
        if task_group_qs.count() > 0:
            task_group = task_group_qs[0]
        return task_group
