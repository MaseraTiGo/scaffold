# coding=UTF-8
import time
import base64
import datetime

from infrastructure.utils.common.single import Single
from infrastructure.utils.cache.redis import redis
from abs.middleware.config.loader import LoaderHelper


class ConfigMiddleware(Single):

    flag = 'config'
    _init_ = False

    def _init_create(self):
        if not self._init_:
            config_mapping = {}
            config_qs = LoaderHelper.loading()
            for config in config_qs:
                config_mapping[(config.type, config.key)] = config
            all_config_data = LoaderHelper().data
            for key, value in all_config_data.items():
                for k, v in value["data"].items():
                    if (key, k) not in config_mapping.keys():
                        LoaderHelper.generate(**{"type_desc":value["type_desc"], \
                                                 "type":key, "name":v["name"], "key":k, \
                                                 "value":self.base64encode(v["value"]) if key == "encryption" else v["value"]})
        self._init_ = True

    def base64encode(self, str):
        return base64.b64encode(str.encode('utf-8')).decode("utf-8")

    def base64decode(self, str):
        return base64.b64decode(str.encode('utf-8')).decode("utf-8")

    def _int(self):
        self._loading_time = time.time()

    def _loading(self):
        self._init_create()
        config_qs = LoaderHelper.loading()
        self._int()
        for item in config_qs:
            redis.hset(self.flag, '{}:{}'.format(item.type, item.key), item.value)

    @property
    def is_refresh(self, seconds = 12 * 60 * 60):
        return (time.time() - self._loading_time) > seconds

    def get_value(self, type, key):
        flag_key = '{}:{}'.format(type, key)
        value = redis.hget(self.flag, flag_key)
        if not hasattr(self, '_loading_time') or value is None or self.is_refresh:
            self._loading()
            value = redis.hget(self.flag, flag_key)

        if type == "encryption" and value != "":
            value = self.base64decode(value)
        return '' if value is None else value

    def update_value(self, type, key, value):
        flag_key = '{}:{}'.format(type, key)
        redis.hset(self.flag, flag_key, value)

    def get_all_config(self, **search_info):
        self._loading()
        config_qs = LoaderHelper.loading()
        return config_qs

    def get_config(self, type, key):
        return LoaderHelper.get_config(type, key)

    def get_data_filter_time(self):
        data_filter_time = int(self.get_value('common', 'data_filter_time'))
        if data_filter_time > 0:
            now_time = datetime.datetime.now()
            start_time = now_time - datetime.timedelta(days = data_filter_time - 1)
            start_time = datetime.datetime.combine(start_time, datetime.time.min)
            return start_time
        return None

    def get_min_time(self, min_time = None):
        data_filter_time = self.get_data_filter_time()
        if not min_time:
            return data_filter_time
        elif not data_filter_time:
            return min_time
        else:
            if data_filter_time > min_time:
                min_time = data_filter_time
        return min_time

config_middleware = ConfigMiddleware()


