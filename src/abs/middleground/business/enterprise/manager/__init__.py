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
            license_number = "91420100MA4KM4XY1Y"
        )
        if company_qs.count() > 0:
            return company_qs[0]
        raise BusinessError('crm总控公司不存在！')

    @classmethod
    def create(cls, license_number, **enterprise_infos):
        is_exsited, enterprise = Enterprise.is_exsited(license_number)
        if is_exsited:
            return enterprise
        else:
            enterprise = Enterprise.create(**enterprise_infos)
        return enterprise

    @classmethod
    def get(cls, enterprise_id):
        enterprise = Enterprise.get_byid(enterprise_id)
        if enterprise is None:
            raise BusinessError('公司不存在！')
        return enterprise

    @classmethod
    def search(cls, current_page, **search_info):
        enterprise_qs = Enterprise.search(**search_info)
        splitor = Splitor(current_page, enterprise_qs)
        return splitor

    @classmethod
    def get_byids(cls, id_list, limit = 100):
        if len(id_list) > limit:
            raise BusinessError('搜索id超过上限！')
        enterprise_qs = Enterprise.search(
            id__in = id_list
        )
        return enterprise_qs

    @classmethod
    def update(cls, enterprise_id, **enterprise_infos):
        enterprise = cls.get(enterprise_id)
        if 'license_number' in enterprise_infos:
            license_number = enterprise_infos['license_number']
            is_exsited, exsited_enterprise = Enterprise.is_exsited(
               license_number
            )
            if is_exsited and exsited_enterprise.id != enterprise_id:
                raise BusinessError('该营业执照已存在，不能更新！')

        enterprise.update(**enterprise_infos)
        return enterprise
