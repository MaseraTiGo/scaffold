# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import EnterpriseGenerator
from abs.middleground.technology.permission.utils.constant import PermissionTypes, \
        UseStatus
from abs.middleground.technology.permission.store import PlatForm


class PlatformGenerator(BaseGenerator):

    def __init__(self, platform_info):
        super(PlatformGenerator, self).__init__()
        self._platform_infos = self.init(platform_info)

    def get_create_list(self, result_mapping):
        company_list = result_mapping.get(EnterpriseGenerator.get_key())
        platform_list = []
        for platform_info in self._platform_infos:
            company_fiter = list(filter(
                lambda obj: obj.name == platform_info.company_name,
                company_list
            ))
            if company_fiter:
                company = company_fiter[0]
                platform_info.update({
                    "company_id":company.id
                })
                platform_list.append(DictWrapper(platform_info))
        return platform_list

    def create(self, platform_info, result_mapping):
        platform_qs = PlatForm.query(
            company_id = platform_info.company_id,
            app_type = platform_info.app_type,
            name = platform_info.name
        )
        if platform_qs.count() > 0:
            platform = platform_qs[0]
        else:
            platform = PlatForm.create(**platform_info)
        return platform

    def delete(self):
        logger.info('================> delete platform <==================')
        return None
