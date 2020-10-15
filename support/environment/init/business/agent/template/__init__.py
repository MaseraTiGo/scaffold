# coding=UTF-8

from src.abs.services.agent.contract.utils.constant import TemplateStatus
from support.common.maker import BaseLoader


class TemplateLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '尚德合同模板0011',
                'status': TemplateStatus.ADOPT,
                'background_img_url': '[{"height": 3508, "path_url": "http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source'
                                      '/contract/template/3545_1601346474.jpg", "width": 2480, "page_number": 1},'
                                      ' {"height": 3508, "path_url": "http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source'
                                      '/contract/template/4700_1601346477.jpg", "width": 2480, "page_number": 2}]'
            }
        ]
