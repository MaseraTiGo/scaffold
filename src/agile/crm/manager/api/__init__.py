# coding=UTF-8

from agile.base.api import AuthorizedApi
from abs.middleware.token import TokenManager
from abs.services.crm.staff.manager import StaffServer


class StaffAuthorizedApi(AuthorizedApi):

    def load_token(self, auth_str):
        return TokenManager.get_token(auth_str)

    def load_auth_user(self):
        staff = StaffServer.get(self._user_id)
        return staff
