# coding=UTF-8

import hashlib
from model.store.model_task import TaskGroup, Task
from model.store.model_role import Organization, Operator


class BaseCrawler(object):

    _root_path = None

    def get_name(self):
        raise NotImplementedError("Please to implemented at subclass")

    def generate_tasks(self, task_group):
        raise NotImplementedError("Please to implemented at subclass")

    def execute_task(self, task_group):
        raise NotImplementedError("Please to implemented at subclass")

    def create_customer_infos(self, organization, operator):
        organization = Organization.create(**organization)
        operator = Operator.create(organization=organization, **operator)
        return organization

    def create_task_group(self):
        name = self.get_name()
        exec_cls = self.get_exec_cls()
        task_group = TaskGroup.create(name=name, exec_cls=exec_cls)
        return task_group

    def get_task_name(self, url):
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def generate_url(self, url):
        assert self._root_path is not None
        return self._root_path + url

    def is_generate_task(self):
        return True

    def get_exec_cls(self):
        return self.__class__.__module__

    def get_undone_tasks(self, group):
        return group.get_undone_tasks()

    def get_undone_group(self):
        exec_cls = self.get_exec_cls()
        task_groups = TaskGroup.query_unexec_task_group(exec_cls)
        return task_groups

    def is_undone(self):
        task_groups = self.get_unexec_tasks()
        return True if task_groups else False

    def store_tasks(self, group, shop_parms_list):
        task_list = []
        for shop in shop_parms_list:
            name = self.get_task_name(shop.url)
            exec_parms = json.dumps({
                'name': shop.name,
                'city': shop.city,
                'url': shop.url,
            })
            task = self.create_task(name=name, group=group, exec_parms=exec_parms)
            if task:
                task_list.append(task)

        return task_list

    def create_task(self, group, name, exec_parms):
        try:
            return Task.create(name=name, group=group, exec_parms=exec_parms)
        except Exception as e:
            print('e : {}'.format(e))
            return None

    def init(self):
        task_group = self.get_undone_group()

        if task_group is None:
            task_group = self.create_task_group()
            task_group.generatting()

        if task_group.is_generatting():
            self.generate_tasks(task_group)
            task_group.generated()

        return True

    def run(self, task_group):
        # add condition to control
        if task_group.generated() or task_group.executting():
            task_group.executting()
            undone_tasks = task_group.get_undone_tasks()
            for undone_task in undone_tasks:
                self.run_task(task_group, undone_task)
            task_group.finished()

    def run_task(self, group, task):
        if not task.is_init():
            return None

        task.executting()
        try:
            self.execute_task(group, task)
            task.finished()
        except Exception as e:
            task.failed(e)
