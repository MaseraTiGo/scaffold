# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import EnterpriseGenerator, \
        StaffGenerator, StaffAccountGenerator
from support.environment.common.middleground.person import PersonMaker
from support.environment.common.middleground.production import ProductionMaker
from support.environment.common.middleground.permission import PermissionMaker
from support.environment.init.business.controller.enterprise import EnterpriseLoader
from support.environment.init.business.crm.staff import StaffLoader


class CrmInitializeMaker(BaseMaker):
    """
    仅仅管理crm初始化的数据
    1、企业数据
    2、部门数据
    3、角色数据
    4、员工及员工账号数据
    5、产品数据
    6、商品数据
    """

    def __init__(self):
        self._person = PersonMaker(StaffLoader().generate()).generate_relate()
        self._production = ProductionMaker().generate_relate()
        self._permission = PermissionMaker().generate_relate()
        self._enterprise = EnterpriseGenerator(EnterpriseLoader().generate())
        self._staff = StaffGenerator(StaffLoader().generate())
        self._staff_account = StaffAccountGenerator()

    def generate_relate(self):
        self._person.add_outputs(self._permission)
        self._staff.add_outputs(self._staff_account)
        self._staff.add_inputs(self._enterprise, self._person)
        self._enterprise.add_outputs(self._production, self._permission)
        return self._staff


if __name__ == "__main__":
    CrmInitializeMaker().run()
