# coding=UTF-8

import time
import collections

from abs.middleware.oss.apihelper import OSSAPI


class OSSRegister(object):

    CRM_OSS = "bq-crm"

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(OSSRegister, cls).__new__(cls, *args, **kwargs)
            cls._register = collections.OrderedDict()
        return cls._instance

    def register(self, entity):
        if entity.name not in self._register:
            self._register[entity.name] = entity
        else:
            raise Exception("The {} bucket have register.".format(entity.name))

    def get_entity(self, module):
        if module in self._register:
            return self._register[module]
        raise Exception("The {} module is not exist for oss.".format(module))

    def get_all_entity(self):
        return self._register.values()

    def get_bucket(self, module):
        return self.get_entity(module).bucket


class OSSHelper(object):

    def __init__(self):
        self.register = OSSRegister()
        self.api = OSSAPI()

    def get_store_file_name(self, store_name, store_module):
        name_fmt = "{module}-{file_name}-{timestamp}"
        suffix_fmt = ".{suffix}"
        split_list = store_name.split('.', -1)

        file_name = name_fmt.format(module = store_module, \
                file_name = split_list[0], timestamp = int(time.time()))
        if len(split_list) > 1:
            file_name += suffix_fmt.format(suffix = split_list[1])

        return file_name

    def put_object(self, file, store_module):
        store_name = self.get_store_file_name(file.name, store_module)
        return self.put_object_byIO(store_name, file, store_module)

    def put_object_byIO(self, store_name, file, store_module):
        bucket_name = self.register.get_bucket(store_module)
        return self.api.put_object(store_name, file, bucket_name)


class OSSEntity(object):

    def __init__(self, name, bucket, desc, is_show = True):
        self.name = name
        self.bucket = bucket
        self.desc = desc
        self.is_show = is_show


oss_helper = OSSHelper()
oss_register = OSSRegister()

oss_list = [
    OSSEntity("crm", OSSRegister.CRM_OSS, "用于存储crm数据"),
]

for oss_entity in oss_list:
    oss_register.register(oss_entity)
