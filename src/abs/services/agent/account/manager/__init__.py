# coding=UTF-8


from abs.middleground.business.account.manager import AccountServer
from abs.middleground.business.account.utils.constant import PlatformTypes
from abs.services.agent.account.store import StaffAccount


class AgentStaffAccountServer(AccountServer):

    APPLY_CLS = StaffAccount
