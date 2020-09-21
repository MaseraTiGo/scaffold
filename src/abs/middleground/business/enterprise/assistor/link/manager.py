# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.manager import EnterpriseServer


class AbstractCompanyServer(BaseManager):

    COMPANY_MODEL = None

    @classmethod
    def create(cls, **enterprise_infos):
        enterprise = EnterpriseServer.create(
            **enterprise_infos
        )
        is_exsited, company = cls.COMPANY_MODEL.is_exsited(
            enterprise_infos["license_number"]
        )
        if is_exsited:
            return company
        else:
            company = cls.COMPANY_MODEL.create(
                company_id=enterprise.id,
                **enterprise_infos
            )
            return company

    @classmethod
    def get(cls, company_id):
        company = cls.COMPANY_MODEL.get_byid(company_id)
        if company is None:
            raise BusinessError('公司不存在！')
        return company

    @classmethod
    def search(cls, current_page, **search_info):
        company_qs = cls.COMPANY_MODEL.search(**search_info)
        splitor = Splitor(current_page, company_qs)
        return splitor

    @classmethod
    def get_byids(cls, id_list, limit=100):
        if len(id_list) > limit:
            raise BusinessError('搜索id超过上限！')
        company_qs = cls.COMPANY_MODEL.search(
            id__in=id_list
        )
        return company_qs

    @classmethod
    def update(cls, company_id, **company_infos):
        company = cls.get(company_id)
        if 'license_number' in company_infos:
            license_number = company_infos['license_number']
            is_exsited, exsited_company = cls.COMPANY_MODEL.is_exsited(
               license_number
            )
            if is_exsited and exsited_company.id != company_id:
                raise BusinessError('该营业执照已存在，不能更新！')

        company.update(**company_infos)
        EnterpriseServer.update(company.company_id, **company_infos)
        return company
