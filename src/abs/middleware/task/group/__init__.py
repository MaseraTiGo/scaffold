# coding=UTF-8

import time
import json
import datetime
import threading

from infrastructure.utils.cache.redis import redis

from infrastructure.utils.cache.local import Local
from infrastructure.utils.common.single import Single


class GroupRegister(Single):

    def __init__(self):
        self._task_mapping = {}

    def register_task(self, task_group):
        self._task_mapping[task_group.get_lable()] = task_group

    def get_task_mapping(self):
       return self._task_mapping


group_register = GroupRegister()
