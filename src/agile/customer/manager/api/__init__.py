# coding=UTF-8

from agile.base.api import AuthorizedApi
from abs.middleware.token import TokenManager
from abs.services.customer.personal.manager import CustomerServer


class CustomerAuthorizedApi(AuthorizedApi):

    def load_token(self, auth_str):
        token = TokenManager.get_token(auth_str)
        return token

    def load_auth_user(self):
        customer = CustomerServer.get(self._user_id)
        return customer
