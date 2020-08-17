# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import EnterpriseGenerator
from abs.middleground.technology.permission.utils.constant import PermissionTypes, \
        UseStatus
from abs.middleground.technology.permission.store import PlatForm


class PlatformGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        company_list = result_mapping.get(EnterpriseGenerator.get_key())
        platform_list = []
        for company in company_list:
            if "必圈" in company.name:
                platform_info = {
                   "name":"教育crm管理平台",
                   "company_id":company.id,
                   "app_type":PermissionTypes.POSITION,
                   "use_status":UseStatus.ENABLE,
                   "prefix":"必圈",
                }
                platform_list.append(DictWrapper(platform_info))
            else:
                pass
        return platform_list

    def create(self, platform_info, result_mapping):
        platform_qs = PlatForm.query(
            company_id = platform_info.company_id,
            app_type = platform_info.app_type,
        )
        if platform_qs.count() > 0:
            platform = platform_qs[0]
        else:
            platform = PlatForm.create(**platform_info)
        return platform

    def delete(self):
        logger.info('================> delete platform <==================')
        return None
