# coding=UTF-8

from support.common.maker import BaseLoader
from abs.middleground.technology.permission.utils.constant import \
        PermissionTypes


class PlatformLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '尚德教育',
                'app_type': PermissionTypes.POSITION,
                'company_name': '尚德教育',
                'remark': "尚德教育代理商平台",
            },
        ]
