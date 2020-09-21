# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import EnterpriseGenerator, \
     PlatformGenerator
from abs.middleground.technology.permission.store import Authorization


class AuthorizationGenerator(BaseGenerator):

    def __init__(self, authorization_info):
        super(AuthorizationGenerator, self).__init__()
        self._authorization_infos = self.init(authorization_info)

    def get_create_list(self, result_mapping):
        company_list = result_mapping.get(EnterpriseGenerator.get_key())
        company_mapping = {
            company.name: company
            for company in company_list
        }
        platform_list = result_mapping.get(PlatformGenerator.get_key())
        platform_mapping = {
            platform.name: platform
            for platform in platform_list
        }

        authorization_list = []
        for authorization_info in self._authorization_infos:
            company = company_mapping.get(
                authorization_info['company_name']
            )
            platform = platform_mapping.get(
                authorization_info['platform_name']
            )
            if company and platform:
                authorization_info.update({
                    "company_id": company.id,
                    "platform": platform
                })
                authorization_list.append(DictWrapper(
                    authorization_info)
                )
        return authorization_list

    def create(self, authorization_info, result_mapping):
        authorization_qs = Authorization.query(
            company_id=authorization_info.company_id,
            platform=authorization_info.platform,
        )
        if authorization_qs.count() > 0:
            authorization = authorization_qs[0]
        else:
            authorization = Authorization.create(
                **authorization_info
            )
        return authorization

    def delete(self):
        logger.info('=============> delete authorization <===============')
        return None
