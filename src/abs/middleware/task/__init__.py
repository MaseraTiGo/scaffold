# coding=UTF-8

import time
import json
import datetime
import threading

from infrastructure.utils.cache.redis import redis
from infrastructure.utils.cache.local import Local
from infrastructure.utils.common.single import Single

from abs.middleware.task.loader import TaskHelper
from abs.middleware.task.group import group_register


class TaskMiddleware(Single):

    redis_store_key = "task_list"
    _task_mapping = {}

    def __init__(self):
        self._loading_time = time.time()
        self._loading()
        self._task_mapping = group_register.get_task_mapping()
        print("============task_mapping===", self._task_mapping.keys(), type(self._task_mapping))

    def _loading(self):
        task_container_list = TaskHelper.loading()
        for task_container in task_container_list:
            self._generate_redis(task_container)
        print("=====task_redis=====>>>初始化", len(task_container_list))

    def force_refresh(self):
        print("=====task_redis=====>>>刷新缓存")
        self._loading()
        return True

    @property
    def is_refresh(self, seconds = 5 * 60):
        return (time.time() - self._loading_time) > seconds

    def _set_redis(self, key, value):
        redis.set(key, json.dumps(value))

    def _get_redis(self, key):
        if not hasattr(self, '_loading_time') or self.is_refresh:
            self._loading_time = time.time()
            self._loading()
        try:
            value = redis.get(key)
            return json.loads(value)
        except Exception as e:
            task_container = TaskHelper.get_container_byname(key)
            if task_container is not None:
                self._generate_redis(task_container)

    def _generate_redis(self, task_container):
        task_container_mapping = {}
        task_container_mapping["id"] = task_container.id
        task_container_mapping["name"] = task_container.name
        task_container_mapping["status"] = task_container.status
        task_container_mapping["lable_list"] = []
        group_list = json.loads(task_container.group_list)
        for group in group_list:
            task_container_mapping["lable_list"].append(group["lable"])
            task_container_mapping[group["lable"]] = {}
            task_container_mapping[group["lable"]]["is_thread"] = True if TaskHelper.check_task_group_exist(container = task_container, \
                                                                                  name = group["name"]) else False
            task_container_mapping[group["lable"]]["lable"] = group["lable"]
            task_container_mapping[group["lable"]]["status"] = "init"
            task_container_mapping[group["lable"]]["type"] = group["type"]
            task_container_mapping[group["lable"]]["name"] = group["name"]
            task_container_mapping[group["lable"]]["exec_parms"] = json.loads(group["exec_parms"])
        self._set_redis(task_container.name, task_container_mapping)
        self._generate_threading(task_container_mapping)

    def update_container_redis(self, name):
        task_container = TaskHelper.get_container_byname(name)
        if task_container is not None:
            self._generate_redis(task_container)

    def _generate_threading(self, task_container_mapping):
        if task_container_mapping["status"] == "init":
            task_container = TaskHelper.update(task_container_mapping["id"], "executting")
            task_container_mapping["status"] = "executting"
            self._set_redis(task_container_mapping["name"], task_container_mapping)
            task_thread = threading.Thread(target = self._run_task_container, \
                                           name = task_container_mapping["name"], \
                                           args = (task_container,))
            task_thread.start()

    def _run_task_container(self, task_container):
        print("===========进入任务容器")
        while True:
            value = self._get_redis(task_container.name)
            print("===========进入任务容器", value)
            if value["status"] == "suspending" or value["status"] == "suspend":
                print("========暂停rrrrrrrrrr", value)
                is_all_task_group_suspend = True
                for lable in value["lable_list"]:
                    if value[lable]["status"] != "suspend":
                        is_all_task_group_suspend = False
                if is_all_task_group_suspend:
                    task_container.update(status = "suspend")
                time.sleep(2)
                continue
            elif value["status"] == "canceling" or value["status"] == "cancel":
                print("========取消rrrrrrrrr", value)
                is_all_task_group_cancel = True
                for lable in value["lable_list"]:
                    if value[lable]["status"] != "cancel":
                        is_all_task_group_cancel = False
                if is_all_task_group_cancel:
                    task_container.update(status = "cancel")
                break
            # self._check_task_group(value)
            print("=======进入任务容器执行")
            for lable in value["lable_list"]:
                if not value[lable]["is_thread"]:
                    print("===========执行任务组", self._task_mapping.keys())
                    print("===>>>>>>>>>>>>>>>>>最后", lable)
                    if lable in self._task_mapping.keys():
                        print("===>>>>>>>>>>>>>>>>>最后")
                        self._task_mapping[lable].run(task_container, **value[lable])
            time.sleep(5)
    '''
    def _check_task_group(self, task_container_redis):
        has_new = False
        task_container = None
        for lable in task_container_redis["lable_list"]:
            if not task_container_redis[lable]["is_thread"]:
                if not has_new:
                    task_container = TaskHelper.get(task_container_redis["id"])
                    has_new = True
                print("=====生成任务组====")
                task_group = TaskHelper.generate_task_group(container = task_container, lable = lable, \
                                               name = task_container_redis[lable]["name"], \
                                               exec_parms = task_container_redis[lable]["exec_parms"], \
                                               status = "executting")
                task_thread = threading.Thread(target = self._task_group_run, name = lable, \
                                               args = (task_container_redis["name"], task_group))
                task_thread.start()

                task_container_redis[lable]["status"] = "executting"
                task_container_redis[lable]["is_thread"] = True
            else:
                print("=====不生成任务组====")

        if has_new:
            self._set_redis("test", task_container_redis)
    '''
    '''
    def _task_group_run(self, reids_name, task_group):
        print("======进入喽", reids_name, task_group)
        value = ""
        while True:
            value = self._get_redis(reids_name)
            if value["status"] == "suspending" or value["status"] == "suspend":
                if task_group.status != "suspend":
                    if task_group.update(status = "suspend"):
                        task_group.status = "suspend"
                        value[task_group.lable]["status"] = "suspend"
                    self._set_redis(reids_name, value)
                time.sleep(2)
                continue
            elif value["status"] == "canceling" or value["status"] == "cancel":
                task_group.update(status = "cancel")
                break
            else:
                if task_group.status != "executting":
                    if task_group.update(status = "executting"):
                        task_group.status = "executting"
                        value[task_group.lable]["status"] = "executting"
                    self._set_redis(reids_name, value)
                time.sleep(2)
                print("=====方法执行完=====")

        value[task_group.lable]["is_thread"] = False
        print("============genxin==", type(reids_name), value)
        self._set_redis(reids_name, value)
        print("==========执行完", value)
    '''

task_middleware = TaskMiddleware()
