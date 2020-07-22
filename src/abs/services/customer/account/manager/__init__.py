# coding=UTF-8


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
