# coding=UTF-8

from infrastructure.utils.common.dictwrapper import DictWrapper
from infrastructure.log.base import logger
from model.store.model_staff import Department
from support.generator.base import BaseGenerator


class DepartmentGenerator(BaseGenerator):

    def __init__(self, department_info):
        super(DepartmentGenerator, self).__init__()
        self._department_infos = self.init(department_info)

    def get_create_list(self, result_mapping):
        return self._department_infos

    def create(self, department_info, result_mapping):
        department_qs = Department.query().filter(name = department_info.name)
        if department_qs.count():
            department = department_qs[0]
        else:
            if department_info.parent:
                parent = Department.query(name = department_info.parent)[0]
                department_info.parent_id = parent.id
            else:
                department_info.parent_id = 0
            department = Department.create(**department_info)
        return department

    def delete(self):
        print('======================>>> delete department <======================')
        return None
