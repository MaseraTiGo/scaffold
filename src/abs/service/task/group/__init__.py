# coding=UTF-8

'''
Created on 2018年8月16日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import Q
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from model.store.model_task import TaskGroup



class TaskGroupHelper(object):

    @classmethod
    def add(cls, **attrs):
        """添加任务组"""
        task_group = TaskGroup.create(**attrs)
        if not task_group:
            raise BusinessError("任务组添加失败")
        return task_group

    @classmethod
    def search_qs(cls, **search_info):
        """查询任组列表"""
        task_group_qs = TaskContainer.search(**search_info)
        return task_group_qs

    @classmethod
    def get(cls, task_group_id):
        """根据id查询任务组详情"""
        task_group = TaskGroup.get_byid(task_group_id)
        if task_group is None:
            raise BusinessError("该任务组不存在")

        return task_group

    @classmethod
    def _update(cls, task_group, **attrs):
        """更新任务组信息"""
        task_group = task_group.update(**attrs)
        return task_group

    @classmethod
    def update_byid(cls, task_group_id, **attrs):
        """通过id更新任务组信息"""
        task_group = cls.get(task_group_id)
        task_group = cls._update(task_group, **attrs)
        return task_group

    @classmethod
    def remover_byid(cls, task_group_id):
        """通过id删除任务组信息"""
        task_group = cls.get(task_group_id)
        task_group.delete()
        return True

    @classmethod
    def hung_group_bycontainer(cls, container):
        """"任务容器挂载任务组"""
        task_group_qs = cls.search_qs(container = container)
        container.group_list = task_group_qs
        return container

    @classmethod
    def hung_group_bycontainerlist(cls, container_list):
        """任务容器批量挂载任务组"""
        container_list_mapping = {}
        for container in container_list:
            container.group_list = []
            container_list_mapping[container.id] = container

        task_group_qs = cls.search_qs(container_id__in = container_list_mapping.keys())
        for task_group in task_group_qs:
            if task_group.container_id in container_list_mapping:
                container_list_mapping[task_group.container_id].group_list.append(task_group)

        return container_list

