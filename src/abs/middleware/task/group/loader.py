# coding=UTF-8
import datetime

from django.db.models import *

from model.store.model_task import TaskGroup

class TaskGroupHelper(object):

    @classmethod
    def generate(cls, **attr):
        """添加任务组"""
        task_group = TaskGroup.create(**attr)
        return task_group

    @classmethod
    def get(cls, task_group_lable):
        """通过任务标签获取任务组"""
        task_group = TaskGroup.search(lable = task_group_lable)
        return task_group
