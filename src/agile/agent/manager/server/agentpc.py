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
from agile.crm.apis.staff import Add, Get, Update, Search
agent_pc_service.add(Add, Get, Update, Search)
