# coding=UTF-8
import random

from support.common.generator.base import BaseGenerator
from support.common.generator.helper import EnterpriseGenerator
from support.common.generator.helper.middleground.merchandise import \
    MerchandiseGenerator
from support.common.generator.helper.business.crm.university.years import \
    YearsGenerator
from support.common.generator.helper.business.agent.template import TemplateGenerator
from abs.services.agent.contract.store.template import TemplateParam


class TemplateParamGenerator(BaseGenerator):

    def __init__(self, template_param_info):
        super(TemplateParamGenerator, self).__init__()
        self._template_param_info = self.init(template_param_info)

    def get_create_list(self, result_mapping):
        template_list = result_mapping.get(TemplateGenerator.get_key())
        template_param_list = []
        for template_param_info in self._template_param_info:
            template = random.choice(template_list)
            template_param_info.update({
                'template': template,
            })
            template_param_list.append(template_param_info)
        return template_param_list

    def create(self, template_param_info, result_mapping):
        template_qs = TemplateParam.search(
            template_id=template_param_info['template'].id,
            param_id=template_param_info['param_id']
        )
        if template_qs.count() > 0:
            return template_qs[0]
        else:
            template = TemplateParam.create(
                **template_param_info
            )
            return template

    def delete(self):
        print('===================>>> delete template param <====================')
        return None
