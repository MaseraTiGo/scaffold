# coding=UTF-8

from abs.common.manager import BaseManager
from abs.middleware.token import TokenManager
from abs.middleground.business.account.manager import AccountServer
from abs.services.customer.account.store import CustomerAccount, Tripartite


class CustomerAccountServer(AccountServer):

    APPLY_CLS = CustomerAccount

    @classmethod
    def hung_account(cls, customer_list):
        customer_mapping = {
            customer.id: customer
            for customer in customer_list
        }
        account_qs = cls.APPLY_CLS.search(
            role_id__in = customer_mapping.keys()
        )
        for account in account_qs:
            customer_mapping[account.role_id].account = None
            if account.role_id in customer_mapping:
                customer_mapping[account.role_id].account = account
        return customer_list

    @classmethod
    def get_customer_account_byusername(cls, username):
        account = cls.APPLY_CLS.get_byusername(username)
        if account:
            return account
        return None

    @classmethod
    def account_login(cls, account):
        token = TokenManager.generate_token(
            account.role_type,
            account.role_id
        )
        return token

    @classmethod
    def login(cls, username, password):
        token = super().login(username, password)
        return token

    @classmethod
    def create(cls, role_id, username, password):
        token = super().create(role_id, username, password)
        return token

    @classmethod
    def update_phone_unique(cls, role_id, unique_code, phone_system):
        CustomerAccount.search(last_login_phone_unique = unique_code).update(
            last_login_phone_unique = "",
            last_login_phone_system = "other",
        )
        super().update(
            role_id,
            **{"last_login_phone_unique":unique_code,
               "last_login_phone_system":phone_system}
        )

    @classmethod
    def logout(cls, role_id, auth_token):
        super().update(
            role_id,
            **{"last_login_phone_unique":"",
               "last_login_phone_system":"other"}
        )
        super().logout(auth_token)


class TripartiteServer(BaseManager):

    @classmethod
    def get_byopenid(cls, openid, category):
        triprtite = Tripartite.search(
            category = category,
            openid = openid
        ).first()
        return triprtite

    @classmethod
    def create(cls, **info):
        return Tripartite.create(**info)

    @classmethod
    def search_all(cls, **search_info):
        return Tripartite.search(**search_info)
