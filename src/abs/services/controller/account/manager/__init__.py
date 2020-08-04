# coding=UTF-8


from abs.middleground.business.account.manager import AccountServer
from abs.middleground.business.account.utils.constant import PlatformTypes
from abs.services.controller.account.store import StaffAccount


class StaffAccountServer(AccountServer):

    APPLY_CLS = StaffAccount
