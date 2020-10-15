# coding=UTF-8

from support.common.maker import BaseLoader


class AgentLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '尚德教育',
                'license_number': "FaNZhengNiGe250YekanbuDong",
                'remark': '这是最叼的代理的公司',
                'province': '湖北省',
                'city': '武汉市',
                'area': '洪山区',
                'address': '光谷软件园',
                'license_url': 'http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/agent/2516_1601346403.png',
            }
        ]
