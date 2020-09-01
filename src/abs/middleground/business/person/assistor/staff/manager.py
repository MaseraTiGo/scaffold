# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.middleground.business.person.manager import PersonServer


class AbstractStaffServer(BaseManager):

    STAFF_MODEL = None

    @classmethod
    def create(cls, phone, **staff_info):
        is_person_exsited, person = PersonServer.is_exsited(phone)
        if is_person_exsited:
            raise BusinessError('客户已存在，不能创建')

        person = PersonServer.create(phone=phone, **staff_info)
        company = EnterpriseServer.get_main_company()
        staff = cls.STAFF_MODEL.create(
            person_id=person.id,
            company_id=company.id,
            phone=phone,
            **staff_info
        )
        return staff

    @classmethod
    def _hung_permission(cls, staff_list):
        for staff in staff_list:
            staff.department_role_list = []
        return staff_list

    @classmethod
    def get(cls, staff_id):
        """
        获取员工详情
        """
        staff = cls.STAFF_MODEL.get_byid(staff_id)
        PersonServer.hung_persons([staff])
        cls._hung_permission([staff])
        return staff

    @classmethod
    def search(cls, current_page, **search_info):
        staff_qs = cls.STAFF_MODEL.search(**search_info)
        staff_qs.order_by('-create_time')
        splitor = Splitor(current_page, staff_qs)
        PersonServer.hung_persons(splitor.get_list())
        cls._hung_permission(splitor.get_list())
        return splitor

    @classmethod
    def is_exsited(cls, phone):
        is_exsited, staff = cls.STAFF_MODEL.is_exsited(phone)
        return is_exsited, staff

    @classmethod
    def update(cls, staff_id, **update_info):
        staff = cls.get(staff_id)
        PersonServer.update(staff.person_id, **update_info)
        staff.update(**update_info)
        return staff
