# coding=UTF-8

'''
Created on 2016年7月26日

@author: Administrator
'''

import redis

from settings import REDIS_CONF
from infrastructure.utils.common.single import Single

class Redis(Single):

    _default_category = "default"

    def __init__(self):
        pool = redis.ConnectionPool(host = REDIS_CONF['host'], \
            port = REDIS_CONF['port'], max_connections = int(REDIS_CONF['max_connections']))
        self.helper = redis.Redis(connection_pool = pool)

    def generate_key(self, name, category):
        category = category if category != None \
            else self._default_category
        return "{}:{}".format(category, name)

    def set(self, name, value, category = None, ex = None, px = None, nx = False, xx = False):
        name_key = self.generate_key(name, category)
        return self.helper.set(name_key, value, ex, px, nx, xx)

    def get(self, name, category = None):
        name_key = self.generate_key(name, category)
        return self.helper.get(name_key).decode('utf-8')

    def delete(self, name, category = None):
        name_key = self.generate_key(name, category)
        return self.helper.delete(name_key)

    def hset(self, name, key, value):
        return self.helper.hset(name, key, value)

    def hget(self, name, key):
        data = self.helper.hget(name, key)
        return None if data is None else data.decode()

    def mget(self, name_list, category = None):
        new_name_list = []
        for key in name_list:
            name_key = self.generate_key(key, category)
            new_name_list.append(name_key)

        values = self.helper.mget(new_name_list)
        if values:
            return [ value.decode("utf-8") for value in values ]
        return []

    def ttl(self, name, category = None):
        name_key = self.generate_key(name, category)
        return self.helper.ttl(name_key)


redis = Redis()
