# coding=UTF-8
import random

from support.common.generator.base import BaseGenerator
from support.common.generator.helper import EnterpriseGenerator
from support.common.generator.helper.middleground.merchandise import \
    MerchandiseGenerator
from support.common.generator.helper.business.crm.university.years import \
    YearsGenerator
from support.common.generator.helper.business.crm.agent import AgentGenerator
from abs.services.agent.contract.store.template import Template


class TemplateGenerator(BaseGenerator):

    def __init__(self, template_info):
        super(TemplateGenerator, self).__init__()
        self._template_info = self.init(template_info)

    def get_create_list(self, result_mapping):
        company_list = result_mapping.get(AgentGenerator.get_key())
        template_list = []
        for template_info in self._template_info:
            company = random.choice(company_list)
            template_info.update({
                'agent_id': company.id,
            })
            template_list.append(template_info)
        return template_list

    def create(self, template_info, result_mapping):
        template_qs = Template.search(name=template_info.name)
        if template_qs.count() > 0:
            return template_qs[0]
        else:
            template = Template.create(
                **template_info
            )
            return template

    def delete(self):
        print('===================>>> delete template <====================')
        return None
