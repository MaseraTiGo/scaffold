# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import EnterpriseGenerator,\
        StaffGenerator, StaffAccountGenerator
from support.environment.init.crm.enterprise import EnterpriseLoader
from support.environment.init.crm.staff import StaffLoader


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
        self._enterprise = EnterpriseGenerator(EnterpriseLoader().generate())
        self._staff = StaffGenerator(StaffLoader().generate())
        self._staff_account = StaffAccountGenerator()

    def generate_relate(self):
        self._staff.add_outputs(self._staff_account)
        self._staff.add_inputs(self._enterprise)

    def generate(self):
        self._enterprise.generate()
        return self._enterprise


if __name__ == "__main__":
    CrmInitializeMaker().run()
