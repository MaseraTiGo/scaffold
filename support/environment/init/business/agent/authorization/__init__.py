# coding=UTF-8

from support.common.maker import BaseLoader
from abs.middleground.technology.permission.utils.constant import \
        UseStatus


class AuthorizationLoader(BaseLoader):

    def generate(self):
        return [
            {
                'use_status': UseStatus.ENABLE,
                'company_name': '尚德教育',
                'platform_name': "尚德教育",
                'remark': "橙鹿CRM总控授权",
            },
        ]
