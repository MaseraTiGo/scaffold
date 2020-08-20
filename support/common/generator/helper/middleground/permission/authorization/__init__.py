# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import EnterpriseGenerator, \
     PlatformGenerator
from abs.middleground.technology.permission.utils.constant import PermissionTypes, \
        UseStatus
from abs.middleground.technology.permission.store import Authorization


class AuthorizationGenerator(BaseGenerator):

    def __init__(self, authorization_info):
        super(AuthorizationGenerator, self).__init__()
        self._authorization_infos = self.init(authorization_info)

    def get_create_list(self, result_mapping):
        company_list = result_mapping.get(EnterpriseGenerator.get_key())
        platform_list = result_mapping.get(PlatformGenerator.get_key())
        authorization_list = []
        for authorization_info in self._authorization_infos:
            company_fiter = list(filter(
                lambda obj: obj.name == authorization_info.company_name,
                company_list
            ))
            platform_fiter = list(filter(
                lambda obj: obj.name == authorization_info.platform_name,
                platform_list
            ))
            if company_fiter and platform_fiter:
                company = company_fiter[0]
                platform = platform_fiter[0]
                authorization_info.update({
                    "use_status":UseStatus.ENABLE,
                    "company_id":company.id,
                    "platform":platform
                })
                authorization_list.append(DictWrapper(authorization_info))
        return authorization_list

    def create(self, authorization_info, result_mapping):
        authorization_qs = Authorization.query(
            company_id = authorization_info.company_id,
            platform = authorization_info.platform,
        )
        if authorization_qs.count() > 0:
            authorization = authorization_qs[0]
        else:
            authorization = Authorization.create(**authorization_info)
        return authorization

    def delete(self):
        logger.info('================> delete authorization <==================')
        return None
