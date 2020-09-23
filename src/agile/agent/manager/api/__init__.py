# coding=UTF-8

from agile.base.api import AuthorizedApi
from abs.middleware.token import TokenManager
from abs.services.agent.agent.manager import AgentStaffServer
from abs.services.agent.agent.manager import AgentServer


class AgentStaffAuthorizedApi(AuthorizedApi):

    def load_token(self, auth_str):
        return TokenManager.get_token(auth_str)

    def load_auth_user(self):
        staff = AgentStaffServer.get(self._user_id)
        return staff
