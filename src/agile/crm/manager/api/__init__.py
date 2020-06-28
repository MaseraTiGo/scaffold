# coding=UTF-8

from  agile.base.api import AuthorizedApi
from abs.service.staff.manager import StaffServer, StaffTokenServer


class StaffAuthorizedApi(AuthorizedApi):

    def load_token(self, auth_str):
        return StaffTokenServer.get_token(auth_str)

    def load_auth_user(self):
        staff = StaffServer.get_byid(self._user_id)
        return staff

