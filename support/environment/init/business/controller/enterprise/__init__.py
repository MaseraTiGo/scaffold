# coding=UTF-8

from support.common.maker import BaseLoader


class EnterpriseLoader(BaseLoader):

    def generate(self):
        return [{
            'name': '橙鹿教育科技（湖北）有限公司',
            'license_number': "91420100MA49JBFP69",
            'remark': '这是最主要的公司',
            'province':'湖北省',
            'city':'武汉市',
            'area':'洪山区',
            'address':'光谷软件园',
        }]
