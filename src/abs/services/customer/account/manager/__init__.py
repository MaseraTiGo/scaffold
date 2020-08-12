# coding=UTF-8


from abs.middleware.token import TokenManager
from abs.middleground.business.account.manager import AccountServer
from abs.services.customer.account.store import CustomerAccount


class CustomerAccountServer(AccountServer):

    APPLY_CLS = CustomerAccount

    @classmethod
    def hung_account(cls, customer_list):
        customer_mapping = {
            customer.id: customer
            for customer in customer_list
        }
        account_qs = cls.APPLY_CLS.search(
            role_id__in=customer_mapping.keys()
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
    def account_login(cls,  account):
        token = TokenManager.generate_token(
            account.role_type,
            account.role_id
        )
        return token
