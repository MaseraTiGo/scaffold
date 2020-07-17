# coding=UTF-8

import datetime
from support.init.base import BaseLoader


class EnterpriseLoader(BaseLoader):

    def load(self):
        return [{
            'name': '必圈信息技术（湖北）有限公司',
            'license_number': "91420100MA4KM4XY1Y",
            'remark': '这是最主要的公司'
        }]
