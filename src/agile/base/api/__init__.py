# coding=UTF-8


from infrastructure.core.api.base import BaseApi
from infrastructure.core.exception.debug_error import DebugError


class NoAuthrizedApi(BaseApi):

    @classmethod
    def is_auth(cls):
        return False

    def authorized(self, request, parms):
        return parms


class AuthorizedApi(BaseApi):

    _user_id = None
    _auth_flag = "auth"

    def _check_IP(self, token):
        print('check ip ......')

    def _check_time(self, token):
        print('check api timeout ...')

    @property
    def auth_user(self):
        if not hasattr(self, "_auth_user"):
            self._auth_user = self.load_auth_user()
        return self._auth_user

    def authorized(self, request, parms):
        auth_str = parms.pop(self._auth_flag)
        token = self.load_token(auth_str)
        self._user_id = token.user_id
        return parms

    def load_token(self, auth_str):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def load_auth_user(self):
        raise NotImplementedError('Please imporlement this interface in subclass')


