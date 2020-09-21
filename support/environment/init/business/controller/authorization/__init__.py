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
                'platform_name': "中台",
                'remark': "橙鹿授权",
            },
            {
                'use_status': UseStatus.ENABLE,
                'company_name': '必圈信息技术（湖北）有限公司',
                'platform_name': "中台",
                'remark': "必圈信息技术（湖北）有限公司授权",
            },
            {
                'use_status': UseStatus.FORBIDDEN,
                'company_name': '湖北融通汇信网络有限公司',
                'platform_name': "中台",
                'remark': "湖北融通汇信网络有限公司授权",
            },
        ]
