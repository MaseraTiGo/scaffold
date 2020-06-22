# coding=UTF-8
import time
import json
import threading

from infrastructure.utils.common.single import Single
from infrastructure.utils.cache.redis import redis

from abs.middleware.task.group.loader import TaskGroupHelper

class BaseGroup(Single):

    _page_num = 1
    _page_size = 1

    @classmethod
    def get_lable(self):
        return "这是一个任务组标签"

    @classmethod
    def get_desc(self):
        return "这是一个任务组描述"

    @classmethod
    def exec_method(self, **param):
        raise NotImplementedError('Please imporlement this interface in subclass')

    @classmethod
    def generate(self, **attr):
        """添加任务组"""
        return TaskGroupHelper.generate(**attr)

    @classmethod
    def run(self, task_container, **attr):
        print("======来到任务组", attr)
        redis_name = task_container.name
        print("=========", redis_name)
        attr.update({"container":task_container})
        task_group = self.generate(**attr)
        task_thread = threading.Thread(target = self.thread_run, name = task_group.lable, \
                                               args = (redis_name, task_group))
        task_thread.start()
        redis_value = json.loads(redis.get(task_container.name))
        redis_value[attr.get("lable")]["is_thread"] = True
        redis.set(task_container.name, json.dumps(redis_value))

    @classmethod
    def thread_run(self, redis_name, task_group):
        print("===============进入任务组", redis_name)
        page = self._page_num
        while True:
            print("===============进入任务组222", redis_name)
            redis_value = json.loads(redis.get(redis_name))
            print("===============进入任务组333", redis_value, type(redis_value))
            if redis_value["status"] == "suspending" or redis_value["status"] == "suspend":
                print("==============暂停")
                if task_group.status != "suspend":
                    if task_group.update(status = "suspend"):
                        task_group.status = "suspend"
                        redis_value[task_group.lable]["status"] = "suspend"
                    redis.set(redis_name, json.dumps(redis_value))
                time.sleep(2)
                continue
            elif redis_value["status"] == "canceling" or redis_value["status"] == "cancel":
                task_group.update(status = "cancel")
                break
            else:
                print("=========开始执行任务", redis_name)
                if task_group.status != "executting":
                    print("==============取消")
                    if task_group.update(status = "executting"):
                        task_group.status = "executting"
                        redis_value[task_group.lable]["status"] = "executting"
                    print("=======freids_name", redis_name)
                    redis.set(redis_name, json.dumps(redis_value))
                print("======页码=======", page)
                search_info = {"page_num":page, "page_size":self._page_size}
                result = self.exec_method(**search_info)
                if result is None or len(result.data) <= 0:
                    break
                print("=====方法执行完=====", redis_value)
                page = page + 1
            time.sleep(3)

        redis_value[task_group.lable]["is_thread"] = False
        print("============genxin==", type(redis_name), redis_value)
        redis.set(redis_name, json.dumps(redis_value))
        print("==========执行完", redis_value)
