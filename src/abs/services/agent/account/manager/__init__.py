# coding=UTF-8

import json
from abs.middleground.business.account.manager import AccountServer
from abs.middleground.business.account.utils.constant import PlatformTypes
from abs.services.agent.account.store import StaffAccount
from abs.services.agent.agent.store import Staff
from abs.middleground.technology.permission.store.entity.person import PersonPermission
from abs.middleground.technology.permission.store.entity.rule import RuleGroup
from abs.middleground.technology.permission.store.entity.position import Position, PositionPermission


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

    @classmethod
    def hung_rule_codes(cls, user_id):
        try:
            permission_id = Staff.search(id=user_id)[0].permission_id
            content = PositionPermission.search(id=permission_id)[0].position.rule_group.content
        except IndexError:
            content = '[]'
        if '-' in content:
            code_list = []
            for codes in json.loads(content):
                code_list.extend(codes.split('-'))
            return list(set(code_list))
        return json.loads(content)

    @classmethod
    def is_admin(cls, user_id):
        return True if Staff.search(id=user_id).first().is_admin else False
