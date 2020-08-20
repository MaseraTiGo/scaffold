# coding=UTF-8

from support.common.maker import BaseLoader


class AuthorzationLoader(BaseLoader):

    def generate(self):
        return [
            {
                'platform_name': '橙鹿教育科技总控平台',
                'company_name': "橙鹿教育科技（湖北）有限公司",
            }
        ]
