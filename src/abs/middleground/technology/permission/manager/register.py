# coding=UTF-8


from infrastructure.utils.common.dictwrapper import DictWrapper
from infrastructure.utils.common.single import Single
from abs.middleground.technology.permission.models import \
        Authorization
from abs.middleground.technology.permission.manager.organization import \
        OrganizationHelper
from abs.middleground.technology.permission.manager.position import \
        PositionHelper


class PermissionRegister(Single):

    @property
    def platform_mapping(self):
        if not hasattr(self, '_platform_mapping'):
            self._platform_mapping = self.all_refresh()
        return self._platform_mapping

    def load_cache(self, authorization):
        organization = OrganizationHelper(authorization)
        position = PositionHelper(authorization)
        cache = DictWrapper({
            'organization': organization,
            'position': position,
            'authorization': authorization,
            'platform': authorization.platform
        })
        return cache

    def refresh(self, authorization):
        self.platform_mapping.update({
            authorization.appkey: self.load_cache(
                authorization
            )
        })

    def all_refresh(self):
        result = {}
        for authorization in Authorization.query():
            result[authorization.id] = self.load_cache(
                authorization
            )
        return result

    def get_helper(self, authorization):
        if authorization.appkey not in self.platform_mapping:
            self.refresh(authorization)
        return self.platform_mapping[authorization.appkey]


permission_register = PermissionRegister()
