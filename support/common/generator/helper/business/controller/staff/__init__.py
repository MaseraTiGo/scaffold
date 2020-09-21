# coding=UTF-8


from support.common.generator.base import BaseGenerator
from support.common.generator.helper import EnterpriseGenerator,\
        PersonGenerator, AuthorizationGenerator
from abs.middleground.technology.permission.store import \
        Position, PositionPermission, Organization
from abs.services.controller.staff.models import Staff, Company


class ControllerStaffGenerator(BaseGenerator):

    def __init__(self, staff_info):
        super(ControllerStaffGenerator, self).__init__()
        self._staff_infos = self.init(staff_info)

    def get_create_list(self, result_mapping):
        authorization_list = result_mapping.get(
            AuthorizationGenerator.get_key()
        )
        result = {}

        for authorization in authorization_list:
            platform = authorization.platform
            if platform.name not in result:
                result[platform.name] = platform
                platform.company_mapping = {}
            result[platform.name].company_mapping[
                authorization.company_name
            ] = authorization

        enterprise_list = result_mapping.get(EnterpriseGenerator.get_key())
        enterprise_mapping = {
            enterprise.name: enterprise
            for enterprise in enterprise_list
        }
        for staff_info in self._staff_infos:
            platform_name = staff_info.pop("platform")
            company_name = staff_info.pop('company')
            platform = result[platform_name]
            authorization = platform.company_mapping[company_name]
            enterprise = enterprise_mapping.get(company_name)
            staff_info['authorization'] = authorization
            staff_info['permission_key'] = authorization.appkey
            staff_info['enterprise'] = enterprise

        return self._staff_infos

    def create(self, staff_info, result_mapping):
        staff_qs = Staff.query().filter(work_number=staff_info.work_number)
        if staff_qs.count():
            staff = staff_qs[0]
        else:
            person_list = result_mapping.get(PersonGenerator.get_key())
            for person in person_list:
                authorization = staff_info.pop('authorization')
                organization_name = staff_info.pop("organization")
                organization_qs = Organization.query(
                    authorization=authorization,
                    name=organization_name
                )
                position_name = staff_info.pop("position")
                position_qs = Position.query(
                    authorization=authorization,
                    name=position_name
                )
                enterprise = staff_info.pop("enterprise")
                permission_key = staff_info.pop('permission_key')
                company_qs = Company.query().filter(
                    company_id=enterprise.id
                )
                if company_qs.count():
                    company = company_qs[0]
                else:
                    company = Company.create(
                        company_id=enterprise.id,
                        name=enterprise.name,
                        license_number=enterprise.license_number,
                        permission_key=permission_key,
                        remark=enterprise.remark,
                    )
                if organization_qs.count() and position_qs.count():
                    staff = Staff.create(
                        person_id=person.id,
                        company=company,
                        **staff_info
                    )
                    pp = PositionPermission.create(
                        person_id=staff.id,
                        authorization=authorization,
                        organization=organization_qs[0],
                        position=position_qs[0],
                    )
                    staff.update(permission_id=pp.id)
        return staff

    def delete(self):
        print('======================>>> delete staff <======================')
        return None
