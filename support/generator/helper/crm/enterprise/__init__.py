# coding=UTF-8


from support.generator.base import BaseGenerator
from abs.middleground.business.enterprise.models import Enterprise


class EnterpriseGenerator(BaseGenerator):

    def __init__(self, enterprise_info):
        super(EnterpriseGenerator, self).__init__()
        self._enterprise_infos = self.init(enterprise_info)

    def get_create_list(self, result_mapping):
        return self._enterprise_infos

    def create(self, enterprise_info, result_mapping):
        enterprise_qs = Enterprise.query().filter(
            license_number=enterprise_info.license_number
        )
        if enterprise_qs.count():
            enterprise = enterprise_qs[0]
        else:
            enterprise = Enterprise.create(
                **enterprise_info
            )
        return enterprise

    def delete(self):
        print('==================>>> delete enterprise <==================')
        return None
