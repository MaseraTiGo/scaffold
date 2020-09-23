# coding=UTF-8

from support.common.maker import BaseLoader
from abs.middleground.technology.permission.utils.constant import \
        UseStatus


class AuthorizationLoader(BaseLoader):

    def generate(self):
        return [
            {
                'use_status': UseStatus.ENABLE,
                'company_name': '橙鹿教育科技（湖北）有限公司',
                'platform_name': "橙鹿教育CRM总控平台",
                'remark': "橙鹿CRM总控授权",
            },
        ]
