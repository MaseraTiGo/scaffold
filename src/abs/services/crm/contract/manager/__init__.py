# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.crm.contract.models import Param


class ParamServer(BaseManager):

    @classmethod
    def create(cls, **search_info):
        if cls.is_exsited(search_info["name_key"]):
            raise BusinessError("存在重复参数")
        param = Param.create(**search_info)
        if param is None:
            raise BusinessError("合同参数添加失败")
        return param

    @classmethod
    def get(cls, param_id):
        param = Param.get_byid(param_id)
        if param is None:
            raise BusinessError("此参数不存在")
        return param

    @classmethod
    def search(cls, current_page, **search_info):
        param_qs = cls.search_all(**search_info).\
                    order_by("-create_time")
        splitor = Splitor(current_page, param_qs)
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        param_qs = Param.search(**search_info)
        return param_qs

    @classmethod
    def is_exsited(cls, name_key, param = None):
        param_qs = cls.search_all(name_key = name_key)
        if param is not None:
            param_qs = param_qs.exclude(id = param.id)
        if param_qs.count() > 0:
            return True
        return False

    @classmethod
    def update(cls, param_id, **update_info):
        param = cls.get(param_id)
        if not param.is_allowed:
            raise BusinessError("系统生成参数不允许修改")
        if cls.is_exsited(update_info["name_key"], param):
            raise BusinessError("存在重复参数")
        param.update(**update_info)
        return param

    @classmethod
    def remove(cls, param):
        if not param.is_allowed:
            raise BusinessError("系统生成参数不允许删除")
        param.delete()
        return True

    @classmethod
    def huang_param(cls, obj_list):
        obj_mapping = {}
        for obj in obj_list:
            obj.param = None
            if obj.param_id not in obj_mapping:
                obj_mapping[obj.param_id] = []
            obj_mapping[obj.param_id].append(obj)
        param_qs = cls.search_all(id__in = obj_mapping.keys())
        for param in param_qs:
            if param.id in obj_mapping:
                for obj in obj_mapping[param.id]:
                    obj.param = param

        return obj_list
