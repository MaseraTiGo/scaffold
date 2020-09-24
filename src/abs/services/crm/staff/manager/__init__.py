# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.middleground.business.person.assistor.staff.manager import\
        AbstractStaffServer
from abs.middleground.business.enterprise.assistor.link.manager import\
        AbstractCompanyServer
from abs.services.crm.staff.models import Staff, Company


class StaffServer(AbstractStaffServer):

    STAFF_MODEL = Staff

    @classmethod
    def generate_work_number(cls, company):
        count_num = Staff.search(company = company).count()
        work_number = "BQ" + str(10000000 + count_num + 1)
        return work_number


class CompanyServer(AbstractStaffServer):

    COMPANY_MODEL = Company

    @classmethod
    def get_platform_company(cls):
        company = None
        company_qs = Company.search()
        if company_qs.count() > 0:
            company = company_qs[0]
        return company

