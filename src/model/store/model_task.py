# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class TaskContainerStatus(object):
    INIT = "init"
    EXECUTTING = "executting"
    FINISHED = "finished"
    FAILED = "failed"
    SUSPENDING = "suspending"
    SUSPEND = "suspend"
    CANCELING = "canceling"
    CANCEL = "cancel"
    CHOICES = ((INIT, '初始化'), (EXECUTTING, "任务执行中"), (FINISHED, "任务执行完成"), \
               (FAILED, "任务失败"), (SUSPENDING, "任务暂停中"), (SUSPEND, "任务暂停"), \
               (CANCELING, "任务取消中"), (CANCEL, "任务取消"))

class TaskContainerType(object):
    ALWAYS = "always"
    TIME = "time"
    INTERVAL = "interval"
    ONCE = "once"
    CHOICES = ((ALWAYS, '一直执行'), (TIME, "时间段内执行"), (INTERVAL, "间隔时间执行"), \
               (ONCE, "执行一次"))

class TaskContainer(BaseModel):
    name = CharField(verbose_name = "任务容器名称", unique = True, max_length = 64)
    exec_parms = TextField(verbose_name = "执行参数", default = "")
    group_list = TextField(verbose_name = "执行任务项", default = "")
    status = CharField(verbose_name = "任务执行状态", choices = TaskContainerStatus.CHOICES, \
                       max_length = 128, default = TaskContainerStatus.INIT)
    type = CharField(verbose_name = "任务容器类型", choices = TaskContainerType.CHOICES, \
                       max_length = 128, default = TaskContainerType.ALWAYS)
    reason = TextField(verbose_name = "任务失败原因", default = "")
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "task_container"

    @classmethod
    def search(cls, **attrs):
        task_container_qs = cls.query().filter(**attrs)
        return task_container_qs


class GroupStatus(object):
    INIT = "init"
    GENERATTING = "generatting"
    GENERATED = "generated"
    EXECUTTING = "executting"
    SUSPEND = "suspend"
    FINISHED = "finished"
    CANCEL = "cancel"
    CHOICES = ((INIT, '初始化'), (GENERATTING, "任务生成中"), (GENERATED, "任务生成完成"), \
               (EXECUTTING, "任务执行中"), (SUSPEND, "任务暂停"), \
               (FINISHED, "任务执行完成"), (CANCEL, "任务取消"))

class TaskGroupType(object):
    ALWAYS = "always"
    TIME = "time"
    INTERVAL = "interval"
    ONCE = "once"
    CHOICES = ((ALWAYS, '一直执行'), (TIME, "时间段内执行"), (INTERVAL, "间隔时间执行"), \
               (ONCE, "执行一次"))

class TaskGroup(BaseModel):
    container = ForeignKey(TaskContainer, on_delete=CASCADE, null = True)
    lable = CharField(verbose_name = "任务组标示", max_length = 128, default = "")
    name = CharField(verbose_name = "任务组名称", max_length = 64, default = "")
    exec_cls = CharField(verbose_name = "任务组执行类", max_length = 128, default = "")
    exec_parms = TextField(verbose_name = "任务组执行参数", default = "")
    status = CharField(verbose_name = "任务组整体执行状态", choices = GroupStatus.CHOICES, \
                       max_length = 32, default = GroupStatus.INIT)
    type = CharField(verbose_name = "任务组类型", choices = TaskGroupType.CHOICES, \
                       max_length = 128, default = TaskGroupType.ALWAYS)
    reason = TextField(verbose_name = "任务取消原因", default = "")
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "task_group"

    @classmethod
    def search(cls, **attrs):
        task_group_qs = cls.query().filter(**attrs)
        return task_group_qs

    def is_init(self):
        return self.status == GroupStatus.INIT

    def is_generatting(self):
        return self.status == GroupStatus.GENERATTING

    def is_generated(self):
        return self.status == GroupStatus.GENERATED

    def is_executting(self):
        return self.status == GroupStatus.EXECUTTING

    def is_finished(self):
        return self.status == GroupStatus.FINISHED

    def is_cancel(self):
        return self.status == GroupStatus.CANCEL

    def generatting(self):
        return self.update(status = GroupStatus.GENERATTING)

    def generated(self):
        return self.update(status = GroupStatus.GENERATED)

    def executting(self):
        return self.update(status = GroupStatus.EXECUTTING)

    def finished(self):
        return self.update(status = GroupStatus.FINISHED)

    def cancel(self):
        return self.update(status = GroupStatus.CANCEL)

    def get_undone_tasks(self):
        tasks = Task.query_undone_tasks(self)
        return tasks

    @classmethod
    def query_unexec_task_group(cls, exec_cls):
        try:
            return cls.query(exec_cls = exec_cls).filter(status__in = [GroupStatus.INIT, \
                            GroupStatus.GENERATED, GroupStatus.EXECUTTING]).\
                                order_by('-create_time')[0]
        except:
            return None


class TaskStatus(object):
    INIT = "init"
    EXECUTTING = "executting"
    FINISHED = "finished"
    FAILED = "failed"
    CANCEL = "cancel"
    CHOICES = ((INIT, '初始化'), (EXECUTTING, "任务执行中"), (FINISHED, "任务执行完成"), \
               (FAILED, "任务失败"), (CANCEL, "任务取消"))


class Task(BaseModel):
    name = CharField(verbose_name = "任务名称", unique = True, max_length = 64)
    group = ForeignKey(TaskGroup, on_delete=CASCADE)
    exec_parms = TextField(verbose_name = "执行参数", default = "")
    status = CharField(verbose_name = "任务执行状态", choices = TaskStatus.CHOICES, \
                       max_length = 32, default = TaskStatus.INIT)
    reason = TextField(verbose_name = "任务失败原因", default = "")
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "task_info"

    @classmethod
    def query_undone_tasks(cls, group):
        return cls.query(group = group, status = TaskStatus.INIT)

    def is_init(self):
        return self.status == TaskStatus.INIT

    def is_executting(self):
        return self.status == TaskStatus.EXECUTTING

    def is_finished(self):
        return self.status == TaskStatus.FINISHED

    def is_failed(self, reason):
        return self.status == TaskStatus.FAILED

    def is_cancel(self):
        return self.status == TaskStatus.CANCEL

    def executting(self):
        return self.update(status = TaskStatus.EXECUTTING)

    def finished(self):
        return self.update(status = TaskStatus.FINISHED)

    def failed(self, reason):
        return self.update(status = TaskStatus.FAILED)

    def cancel(self):
        return self.update(status = TaskStatus.CANCEL)
