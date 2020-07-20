# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import StaffGenerator, \
        StaffAccountGenerator, EnterpriseGenerator

from support.environment.init.business.crm.enterprise import EnterpriseLoader
from support.environment.simulate.business.crm.staff import CrmStaffLoader


class CrmSimulateMaker(BaseMaker):
    """
    仅仅管理crm需要模拟的数据, 可包括:
    1、企业数据
    2、部门数据
    3、角色数据
    4、员工及员工账号数据
    5、产品数据
    6、商品数据
    """

    def generate_relate(self):
        enterprise = EnterpriseGenerator(EnterpriseLoader().generate())
        staff = StaffGenerator(CrmStaffLoader().generate())
        staff_account = StaffAccountGenerator()

        staff.add_outputs(staff_account)
        staff.add_inputs(enterprise)
        return staff
