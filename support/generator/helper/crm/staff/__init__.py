# coding=UTF-8


from infrastructure.log.base import logger
from model.store.model_staff import Staff
from model.common.model_user_base import UserCertification
from support.generator.base import BaseGenerator


class StaffGenerator(BaseGenerator):

    def __init__(self, staff_info):
        super(StaffGenerator, self).__init__()
        self._staff_infos = self.init(staff_info)

    def get_create_list(self, result_mapping):
        return self._staff_infos

    def create(self, staff_info, result_mapping):
        user_certification_qs = UserCertification.query().filter(
            identification=staff_info.identification
        )
        if user_certification_qs.count():
            user_certification = user_certification_qs[0]
        else :
            user_certification = UserCertification.create(**staff_info)

        staff_qs = Staff.query().filter(id_number = staff_info.id_number)
        if staff_qs.count():
            staff = staff_qs[0]
        else:
            staff = Staff.create(certification = user_certification, **staff_info)
        return staff

    def delete(self):
        print('======================>>> delete staff <======================')
        return None
