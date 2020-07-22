# coding=UTF-8


from abs.middleground.business.account.manager import AccountServer
from abs.services.customer.account.store import CustomerAccount


class CustomerAccountServer(AccountServer):

    APPLY_CLS = CustomerAccount
