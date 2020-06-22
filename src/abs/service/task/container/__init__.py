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

from model.store.model_task import TaskContainer



class TaskContainerHelper(object):

    @classmethod
    def add(cls, **attrs):
        """添加任务容器"""
        task_container = TaskContainer.create(**attrs)
        if not task_container:
            raise BusinessError("任务容器添加失败")
        return task_container

    @classmethod
    def search(cls, current_page, **search_info):
        """查询任务容器列表(分页)"""
        task_container_qs = cls.search_qs(**search_info)
        task_container_qs = task_container_qs.order_by("-create_time")
        return Splitor(current_page, task_container_qs)

    @classmethod
    def search_qs(cls, **search_info):
        """查询任务容器列表"""
        task_container_qs = TaskContainer.search(**search_info)
        return task_container_qs

    @classmethod
    def get(cls, task_container_id):
        """根据id查询任务容器详情"""
        task_container = TaskContainer.get_byid(task_container_id)
        if task_container is None:
            raise BusinessError("该任务容器不存在")

        return task_container

    @classmethod
    def update(cls, task_container, **attrs):
        """更新任务容器信息"""
        task_container = task_container.update(**attrs)
        return task_container

    @classmethod
    def remover(cls, task_container):
        """删除任务容器信息"""
        task_container.delete()
        return True
