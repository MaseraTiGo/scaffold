# coding=UTF-8


from infrastructure.utils.common.dictwrapper import DictWrapper
from infrastructure.utils.common.single import Single
from abs.middleground.technology.permission.models import PlatForm
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

    def load_cache(self, platform):
        organization = OrganizationHelper(platform)
        position = PositionHelper(platform)
        cache = DictWrapper({
            'organization': organization,
            'position': position,
            'platform': platform
        })
        return cache

    def refresh(self, platform):
        self.platform_mapping.update({
            platform.appkey: self.load_cache(platform)
        })

    def all_refresh(self):
        result = {}
        for platform in PlatForm.query():
            result[platform.appkey] = self.load_cache(platform)
        return result

    def get_helper(self, platform):
        if platform.appkey not in self.platform_mapping:
            self.refresh(platform)
        return self.platform_mapping[platform.appkey]


permission_register = PermissionRegister()
