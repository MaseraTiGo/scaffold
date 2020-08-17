# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.middleground.business.person.manager import PersonServer
from abs.services.agent.staff.models import Staff


class AgentStaffServer(BaseManager):

    @classmethod
    def hung_permission(cls, staff_list):
        for staff in staff_list:
            staff.department_role_list = []
        return staff_list

    @classmethod
    def get(cls, staff_id):
        staff = Staff.get_byid(staff_id)
        PersonServer.hung_persons([staff])
        cls.hung_permission([staff])
        return staff

    @classmethod
    def search(cls, current_page, **search_info):
        if "name" in search_info:
            name = search_info.pop("name")
            search_info.update({"name__contains":name})
        staff_qs = Staff.search(**search_info)
        staff_qs.order_by('-create_time')
        splitor = Splitor(current_page, staff_qs)
        PersonServer.hung_persons(splitor.get_list())
        cls.hung_permission(splitor.get_list())
        return splitor

    @classmethod
    def is_exsited(cls, phone):
        is_exsited, staff = Staff.is_exsited(phone)
        return is_exsited, staff

    @classmethod
    def generate_work_number(cls, company_id):
        count_num = Staff.search(company_id = company_id).count()
        work_number = "WN" + str(10000000 + count_num)
        return work_number

    @classmethod
    def create(cls, phone, agent, **staff_info):
        is_person_exsited, person = PersonServer.is_exsited(phone)
        if is_person_exsited:
            raise BusinessError('客户已存在，不能创建')

        person = PersonServer.create(phone = phone, **staff_info)
        staff = Staff.create(
            work_number = cls.generate_work_number(agent.company_id),
            person_id = person.id,
            company_id = agent.company_id,
            agent_id = agent.id,
            phone = phone,
            **staff_info
        )
        return staff

    @classmethod
    def update(cls, staff_id, **update_info):
        staff = cls.get(staff_id)
        is_person_exsited, person = PersonServer.is_exsited(
            update_info["phone"]
        )
        if is_person_exsited:
            if person.id != staff.person_id:
                raise BusinessError('手机号已存在')
        PersonServer.update(staff.person_id, **update_info)
        staff.update(**update_info)
        return staff

    @classmethod
    def hung_staff(cls, obj_list):
        obj_mapping = {}
        for obj in obj_list:
            obj.staff = None
            if obj.staff_id not in obj_mapping:
                obj_mapping[obj.staff_id] = []
            obj_mapping[obj.staff_id].append(obj)
        staff_qs = Staff.search(id__in = obj_mapping.keys())
        for staff in staff_qs:
            if staff.id in obj_mapping:
                for obj in obj_mapping[staff.id]:
                    obj.staff = staff
        return obj_list
