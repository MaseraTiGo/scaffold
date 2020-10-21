# coding=UTF-8

import json
from src.abs.services.agent.contract.utils.constant import TemplateStatus
from support.common.maker import BaseLoader


class TemplateLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '橙鹿教育合同模板001',
                'status': TemplateStatus.ADOPT,
                'background_img_url': '[{"page_number": 1, "path_url": '
                                      '"http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/contract/template/'
                                      '5086_1603088317.jpg", "width": 2480, "height": 3508}, {"page_number": 2, '
                                      '"path_url": "http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/contract/'
                                      'template/9902_1603088320.jpg", "width": 2480, "height": 3508}]'
            }
        ]


class TemplateParamLoder(BaseLoader):

    def generate(self):
        return [
            {
                'param_id': 1,
                'page_number': 1,
                'coordinate_x': 521,
                'coordinate_y': 509,
                'width': 0,
                'content': json.dumps(
                    {"name": "甲方企业名称", "name_key": "agent.name", "key_type": "text", "default_value": "某某有限责任公司",
                     "actual_value_source": "company"}),
                'height': 0,

            },
            {
                'param_id': 2,
                'page_number': 2,
                'coordinate_x': 432,
                'coordinate_y': 2522,
                'width': 484,
                'content': json.dumps({"name": "甲方企业公章", "name_key": "agent.official_seal", "key_type": "image",
                                       "default_value": "https://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/contract/default_official_seal.png",
                                       "actual_value_source": "company"}),
                'height': 481,

            },
            {
                'param_id': 6,
                'page_number': 2,
                'coordinate_x': 1605,
                'coordinate_y': 2435,
                'width': 484,
                'content': json.dumps({"name": "乙方客户手签姓名", "name_key": "autograph", "key_type": "image",
                                       "default_value": "https://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/contract/default_autograph.png",
                                       "actual_value_source": "customer"}),
                'height': 190,

            }
        ]
