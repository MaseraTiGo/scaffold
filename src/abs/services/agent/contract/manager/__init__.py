# coding=UTF-8
import datetime
import json
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.agent.contract.models import Template, TemplateParam


class TemplateServer(BaseManager):

    @classmethod
    def create(cls, **info):
        template = Template.create(**info)
        if template is None:
            raise BusinessError("合同添加失败")
        return template

    @classmethod
    def get(cls, template_id):
        template = Template.get_byid(template_id)
        if template is None:
            raise BusinessError("此合同不存在")
        return template

    @classmethod
    def search(cls, current_page, **search_info):
        template_qs = cls.search_all(**search_info).\
                    order_by("-create_time")
        splitor = Splitor(current_page, template_qs)
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        template_qs = Template.search(**search_info)
        return template_qs

    @classmethod
    def update(cls, template, **update_info):
        template.update(**update_info)
        return template

    @classmethod
    def remove(cls, template):
        TemplateParamServer.search_all(template = template).delete()
        template.delete()
        return True


class TemplateParamServer(BaseManager):

    @classmethod
    def create(cls, **update_info):
        template_param = TemplateParam.create(**search_info)
        if template_param is None:
            raise BusinessError("合同参数添加失败")
        return template_param

    @classmethod
    def batch_create(cls, template, info_list):
        template_param_list = []
        for obj_dic in info_list:
            if obj_dic.param is not None:
                template_param_list.append(TemplateParam(
                    unique_number = TemplateParam.generate_unique_number(),
                    template = template,
                    param_id = obj_dic.param_id,
                    page_number = obj_dic.page_number,
                    coordinate_x = obj_dic.coordinate_x,
                    coordinate_y = obj_dic.coordinate_y,
                    width = obj_dic.width if hasattr(obj_dic, "width") else 0,
                    height = obj_dic.height if hasattr(obj_dic, "height") else 0,
                    content = json.dumps({
                        "name": obj_dic.param.name,
                        "name_key": obj_dic.param.name_key,
                        "key_type": obj_dic.param.key_type,
                        "default_value": obj_dic.param.default_value,
                        "actual_value_source": obj_dic.param.actual_value_source,
                        "actual_value_key": obj_dic.param.actual_value_key,
                    })
                ))
        cls.search_all(template = template).delete()
        TemplateParam.objects.bulk_create(template_param_list)
        return True

    @classmethod
    def search_all(cls, **search_info):
        template_param_qs = TemplateParam.search(**search_info)
        return template_param_qs

    @classmethod
    def get(cls, template_param_id):
        template_param = TemplateParam.get_byid(template_param_id)
        if template_param is None:
            raise BusinessError("此合同配置参数不存在")
        return template_param

    @classmethod
    def update(cls, template_param_id, **update_info):
        template_param = cls.get(template_param_id)
        template_param.update(**update_info)
        return template_param

    @classmethod
    def remove(cls, template_param_id):
        template_param = cls.get(template_param_id)
        template_param.delete()
        return True

    @classmethod
    def huang_for_template(cls, template_list):
        template_mapping = {}
        for template in template_list:
            template.param_list = []
            if template.id not in template_mapping:
                template_mapping[template.id] = template
        template_param_qs = cls.search_all(template_id__in = \
                                           template_mapping.keys())
        for template_param in template_param_qs:
            if template_param.template_id in template_mapping:
                template_mapping[template_param.template_id].\
                    param_list.append(template_param)
        return template_list