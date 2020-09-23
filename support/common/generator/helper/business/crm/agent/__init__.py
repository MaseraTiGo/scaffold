# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper.middleground.enterprise import \
     EnterpriseGenerator

from abs.services.agent.agent.models import Agent


class AgentGenerator(BaseGenerator):

    def __init__(self, agent_infos):
        super(AgentGenerator, self).__init__()
        self._agent_infos = self.init(agent_infos)

    def get_create_list(self, result_mapping):
        agent_list = []
        enterprise_list = result_mapping.get(EnterpriseGenerator.get_key())
        for agent_infos in self._agent_infos:
            enterprise_fiter = list(filter(
                lambda obj: obj.name == agent_infos.name,
                enterprise_list
            ))
        if enterprise_fiter:
            enterprise = enterprise_fiter[0]
            agent_infos.update({
                'company_id': enterprise.id,
            })
            agent_list.append(agent_infos)
        return agent_list

    def create(self, agent_info, result_mapping):
        agent_qs = Agent.query(
            name = agent_info.name,
        )
        if agent_qs.count():
            agent = agent_qs[0]
        else:
            agent = Agent.create(**agent_info)
        return agent

    def delete(self):
        logger.info('================> delete agent <==================')
        return None
