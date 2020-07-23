# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.models import Enterprise


class EnterpriseServer(BaseManager):

    @classmethod
    def get_main_company(cls):
        return cls.get_crm__company()

    @classmethod
    def get_crm__company(cls):
        company_qs = Enterprise.search(
            license_number="91420100MA4KM4XY1Y"
        )
        if company_qs.count() > 0:
            return company_qs[0]
        raise BusinessError('缺少客户的打款公司信息！')

    @classmethod
    def create(cls, **enterprise_infos):
        enterprise = Enterprise.create(**enterprise_infos)
        return enterprise

    @classmethod
    def get(cls, enterprise_id):
        enterprise = Enterprise.get_byid(enterprise_id)
        return enterprise

    @classmethod
    def search(cls, current_page, **search_info):
        enterprise_qs = Enterprise.search(**search_info)
        splitor = Splitor(current_page, enterprise_qs)
        return splitor

    @classmethod
    def update(cls, enterprise_id, **enterprise_infos):
        enterprise = cls.get(enterprise_id)
        enterprise.update(**enterprise_infos)
        return enterprise
