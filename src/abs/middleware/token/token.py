# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import time
import random

from infrastructure.utils.cache.redis import redis
from infrastructure.utils.common.dictwrapper import DictWrapper

from infrastructure.core.exception.api_error import ApiCodes, api_errors

class Token(object):

    _key_fmt = "{role}:{user_id}:token"
    _token_fmt = "{role}:{user_id}{timestamp}{random_num}"
    _unique_key = "unique_key"

    _cache_category = "token"

    def __init__(self, token):
        self.user_id = token.user_id
        self.role = token.role
        self.auth_token = token.auth_token
        self.renew_flag = token.renew_flag
        self.expire_time = token.expire_time
        self.last_ip = None
        self.last_terminal = None

    def _check_expire(self, parms):
        cur_time = int(time.time())
        if cur_time > self.expire_time:
            raise api_errors(ApiCodes.INTERFACE_TOKEN_DUE)

    def _check_ip(self, parms):
        pass

    def _check_terminal(self, parms):
        pass

    def check(self, parms):
        self._check_expire(parms)
        self._check_ip(parms)
        self._check_terminal(parms)

    def renew(self, renew_flag):
        if renew_flag == self.renew_flag:
            result = self.calculate(self.role, self.user_id)
            self.auth_token = result.auth_token
            self.renew_flag = result.renew_flag
            self.expire_time = result.expire_time
            self.role = result.role
            self.user_id = result.user_id
            self.store()
            return self
        else:
            self.clear()
            raise api_errors(ApiCodes.INTERFACE_TOKEN_RENEW_ERROR)

    def clear(self):
        self._clear_one_level()
        self._clear_two_level()

    def _clear_one_level(self):
        # one level cache
        redis.delete(self.auth_token, self._cache_category)

    def _clear_two_level(self):
        # two level cache
        # redis.set(self.auth_token, token_str, self._cache_category)
        pass

    def store(self):
        token_str = json.dumps({
            "renew_flag" : self.renew_flag,
            'user_id': self.user_id,
            "expire_time" : self.expire_time,
            "auth_token" : self.auth_token,
            "role" : self.role,
            # self._unique_key : self.get_unique_key()
        })

        # one level cache
        redis.set(self.auth_token, token_str, self._cache_category)

        # two level cache
        # redis.set(self.auth_token, token_str, self._cache_category)

    @classmethod
    def get(cls, auth_str):
        token_str = redis.get(auth_str, cls._cache_category)
        if token_str is None:
            raise api_errors(ApiCodes.INTERFACE_TOKEN_INVALIED)
        return cls(DictWrapper(json.loads(token_str)))

    @classmethod
    def get_unique_key(cls, user):
        return cls._key_fmt.format(user_id = self.user_id)

    @classmethod
    def _get_time_scope(cls, hour = 24):
        cur_time = int(time.time())
        expire_time = cur_time + hour * 60 * 60
        return cur_time, expire_time

    @classmethod
    def calculate(cls, role, user_id):
        cur_time, expire_time = cls._get_time_scope()
        random_num = random.randint(1, 99999)
        token_str = cls._token_fmt.format(role = role, user_id = user_id,\
                           timestamp = cur_time, random_num = random_num)
        token_md5 = hashlib.md5(token_str.encode("utf-8")).hexdigest()
        size = int(len(token_md5) / 2)
        auth_token = token_md5[:size]
        renew_flag = token_md5[size:]

        return DictWrapper({
            "renew_flag" : renew_flag,
            "user_id": user_id,
            "role": role,
            "expire_time" : expire_time,
            "auth_token" : auth_token,
        })

    @classmethod
    def generate(cls, role, user_id):
        calc_result = cls.calculate(role, user_id)
        token = cls(calc_result)
        token.store()
        return token

    def __str__(self):
        return json.dumps({
            "renew_flag": self.renew_flag,
            "auth_token": self.auth_token,
            "expire_time": self.expire_time,
            "role": self.role,
            "user_id": self.user_id
        })
