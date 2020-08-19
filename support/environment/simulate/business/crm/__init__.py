# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import StaffGenerator, \
        StaffAccountGenerator, EnterpriseGenerator, \
        AgentGenerator, ContactsGenerator

from support.environment.common.middleground.person import PersonMaker
from support.environment.common.middleground.production import ProductionMaker
from support.environment.common.middleground.merchandise import MerchandiseMaker
from support.environment.common.business.crm.years import YearsMaker
from support.environment.init.business.controller.enterprise import EnterpriseLoader
from support.environment.simulate.business.crm.staff import CrmStaffLoader
from support.environment.simulate.business.crm.school import CrmSchoolLoader
from support.environment.simulate.business.crm.major import CrmMajorLoader
from support.environment.simulate.business.crm.years import CrmYearsLoader
from support.environment.simulate.business.crm.contacts import CrmAgentContactsLoader


class CrmSimulateMaker(BaseMaker):
    """
    仅仅管理crm需要模拟的数据, 可包括:
    1、企业数据
    2、部门数据
    3、角色数据
    4、员工及员工账号数据
    5、产品数据
    6、学校数据
    7、专业数据
    8、商品数据
    """

    def generate_relate(self):
        staff_info = CrmStaffLoader().generate()
        enterprise = EnterpriseGenerator(EnterpriseLoader().generate())
        agent = AgentGenerator(EnterpriseLoader().generate())
        contacts = ContactsGenerator(CrmAgentContactsLoader().generate())
        production = ProductionMaker().generate_relate()
        staff = StaffGenerator(staff_info)
        staff_account = StaffAccountGenerator()
        person = PersonMaker(staff_info).generate_relate()
        years = YearsMaker(
            CrmSchoolLoader().generate(),
            CrmMajorLoader().generate(),
            CrmYearsLoader().generate()
        ).generate_relate().generate()
        agent.add_outputs(contacts)
        enterprise.add_outputs(production, agent)
        staff.add_outputs(staff_account)
        staff.add_inputs(enterprise, person)
        return staff
