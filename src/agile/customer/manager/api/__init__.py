# coding=UTF-8

from  agile.base.api import AuthorizedApi
from abs.middleware.token import TokenManager
from abs.service.customer.manager import CustomerServer


class CustomerAuthorizedApi(AuthorizedApi):

    def load_token(self, auth_str):
        print("=============>>>>>>  ", auth_str)
        return TokenManager.get_token(auth_str)

    def load_auth_user(self):
        customer = CustomerServer.get_byid(self._user_id)
        return customer
