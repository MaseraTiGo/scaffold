# coding=UTF-8

from agile.base.api import AuthorizedApi
from abs.middleware.token import TokenManager
from abs.services.agent.staff.manager import AgentStaffServer
from abs.services.crm.agent.manager import AgentServer


class AgentStaffAuthorizedApi(AuthorizedApi):

    def load_token(self, auth_str):
        return TokenManager.get_token(auth_str)

    def load_auth_user(self):
        staff = AgentStaffServer.get(self._user_id)
        return staff

    @property
    def auth_agent(self):
        if not hasattr(self, "_auth_agent"):
            staff = self.load_auth_user()
            self._auth_agent = AgentServer.get(staff.agent_id)
        return self._auth_agent