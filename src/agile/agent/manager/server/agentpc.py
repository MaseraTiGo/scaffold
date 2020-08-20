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
from agile.agent.apis.staff.account import Login, Logout, Add
agent_pc_service.add(Login, Logout, Add)

from agile.agent.apis.staff.account.password import Modify
agent_pc_service.add(Modify)

from agile.agent.apis.staff.myself import Get
agent_pc_service.add(Get)

from agile.agent.apis.staff import Search, Add, Get, Update
agent_pc_service.add(Search, Add, Get, Update)

from agile.agent.apis.goods import Get, Search, Add, Update, Setuse, Remove, \
                                   SearchAll, Share
agent_pc_service.add(Get, Search, Add, Update, Setuse, Remove, SearchAll, Share)

from agile.agent.apis.goods.specification import Add, Get, Update, Remove
agent_pc_service.add(Add, Get, Update, Remove)

from agile.agent.apis.major import SearchAll
agent_pc_service.add(SearchAll)

from agile.agent.apis.school import SearchAll
agent_pc_service.add(SearchAll)

from agile.agent.apis.school.relations.years import All
agent_pc_service.add(All)

from agile.agent.apis.production import SearchAll, All
agent_pc_service.add(SearchAll, All)

from agile.agent.apis.order import Search, Get
agent_pc_service.add(Search, Get)

from agile.agent.apis.order.contract import Search
agent_pc_service.add(Search)

from agile.agent.apis.customer import Search
agent_pc_service.add(Search)

from agile.agent.apis.customer.salechance import Search, Add
agent_pc_service.add(Search, Add)

from agile.agent.apis.customer.order import Search
agent_pc_service.add(Search)

from agile.agent.apis.technology.permission.organization import Add, All, Get , \
                                                              Update, Remove
agent_pc_service.add(Add, All, Get, Update, Remove)

from agile.agent.apis.technology.permission.position import Add, All, Get , \
                                                          Update, Remove
agent_pc_service.add(Add, All, Get, Update, Remove)

from agile.agent.apis.goods.poster import Add
agent_pc_service.add(Add)