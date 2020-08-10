# coding=UTF-8


from abs.middleground.business.account.manager import AccountServer
from abs.middleground.business.account.utils.constant import PlatformTypes
from abs.services.agent.account.store import StaffAccount


class AgentStaffAccountServer(AccountServer):

    APPLY_CLS = StaffAccount

    @classmethod
    def hung_account(cls, obj_list):
        obj_mapping = {}
        for obj in obj_list:
            obj.account = None
            obj_mapping[obj.id] = obj
        account_qs = cls.get_byids(
            obj_mapping.keys()
        )
        for account in account_qs:
            if account.role_id in obj_mapping:
                obj_mapping[account.role_id].account = account
        return obj_list