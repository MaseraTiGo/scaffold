# coding=UTF-8
import hashlib

from infrastructure.core.exception.business_error import BusinessError

from infrastructure.core.api.base import BaseApi
from infrastructure.core.exception.debug_error import DebugError

from abs.service.user.manager import UserServer
from abs.service.staff.manager import StaffServer
from agile.apis.base import AuthorizedApi


class ServerAuthorizedApi(AuthorizedApi):

    _auth_token = "BQkhcGMXQDujIXpExAmPLe"

    def authorized(self, request, parms):
        return parms


class MiniAuthorizedApi(ServerAuthorizedApi):

    def authorized(self, request, parms):
        '''
        timestamp = parms["parms"]

        auth_str = "{token}{timestamp}".format(token = self._auth_token, timestamp = timestamp)

        if hashlib.md5(auth_str.encode("utf-8")).hexdigest() != parms["auth"]:
            raise BusinessError("验证失败")
        '''
        return parms
