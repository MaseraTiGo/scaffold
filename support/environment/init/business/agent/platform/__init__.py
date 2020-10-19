# coding=UTF-8

from support.common.maker import BaseLoader
from abs.middleground.technology.permission.utils.constant import \
        PermissionTypes


class PlatformLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '橙鹿教育代理商平台',
                'app_type': PermissionTypes.POSITION,
                'company_name': '橙鹿教育科技（湖北）有限公司',
                'remark': "橙鹿教育代理商平台",
            },
        ]
