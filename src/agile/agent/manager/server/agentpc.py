# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService


class AgentPcService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "用户服务"

    @classmethod
    def get_desc(self):
        return "针对注册登录代理商员工提供服务"

    @classmethod
    def get_flag(cls):
        return "agent-pc"


agent_pc_service = AgentPcService()
from agile.agent.apis.staff.account import Login
agent_pc_service.add(Login)

from agile.agent.apis.staff.account.password import Modify
agent_pc_service.add(Modify)

from agile.agent.apis.staff.myself import Get
agent_pc_service.add(Get)

from agile.agent.apis.staff import Search
agent_pc_service.add(Search)