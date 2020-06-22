# coding=UTF-8

'''
Created on 2016年7月26日

@author: Administrator
'''

import redis

from infrastructure.utils.common.single import Single


class Local(Single):

    _cache = {}
    _default_category = "default"

    def set(self, name, value, category = None):
        category = category if category != None \
            else self._default_category
        if category not in self._cache:
            self._cache[category] = {}
        self._cache[category][name] = value

    def get(self,name, category = None):
        category = category if category != None \
            else self._default_category
        if category not in self._cache:
            return None
        elif name not in self._cache[category]:
            return None
        return self._cache[category][name]

    def delete(self, name, category = None):
        category = category if category != None \
            else self._default_category
        self._cache[category].pop(name)
        if len(self._cache[category]) == 0:
            self._cache.pop(category)


local = Local()
