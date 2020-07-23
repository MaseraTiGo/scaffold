# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import StaffGenerator, \
        StaffAccountGenerator, EnterpriseGenerator

from support.environment.common.middleground.person import PersonMaker
from support.environment.common.middleground.production import ProductionMaker
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
        staff_info = CrmStaffLoader().generate()
        enterprise = EnterpriseGenerator(EnterpriseLoader().generate())
        production = ProductionMaker().generate_relate()
        staff = StaffGenerator(staff_info)
        staff_account = StaffAccountGenerator()
        person = PersonMaker(staff_info).generate_relate()

        staff.add_outputs(staff_account)
        staff.add_inputs(enterprise, person)
        enterprise.add_outputs(production)
        return staff
