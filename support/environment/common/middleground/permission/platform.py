# coding=UTF-8

from support.common.maker import BaseLoader


class PlatformLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '橙鹿教育科技总控平台',
                'company_name': "橙鹿教育科技（湖北）有限公司",
                'app_type':'position',
            },
            {
                'name': '橙鹿教育科技代理商平台',
                'company_name': "橙鹿教育科技（湖北）有限公司",
                'app_type':'position',
            }
        ]
