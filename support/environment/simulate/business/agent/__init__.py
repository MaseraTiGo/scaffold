# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import AgentStaffGenerator, \
        AgentStaffAccountGenerator, EnterpriseGenerator, SchoolGenerator, \
        MajorGenerator, GoodsGenerator, AgentGenerator, ContactsGenerator

from support.environment.common.middleground.person import PersonMaker
from support.environment.common.middleground.production import ProductionMaker
from support.environment.common.middleground.merchandise import MerchandiseMaker
from support.environment.init.business.controller.enterprise import EnterpriseLoader
from support.environment.simulate.business.agent.staff import AgentStaffLoader
from support.environment.simulate.business.crm.school import CrmSchoolLoader
from support.environment.simulate.business.crm.major import CrmMajorLoader
from support.environment.simulate.business.agent.goods import GoodsLoader
from support.environment.simulate.business.crm.contacts import CrmAgentContactsLoader


class AgentSimulateMaker(BaseMaker):
    """
    仅仅管理agent需要模拟的数据, 可包括:
    1、企业数据
    2、部门数据
    3、角色数据
    4、员工及员工账号数据
    5、商品数据
    """

    def generate_relate(self):
        staff_info = AgentStaffLoader().generate()
        goods_info = GoodsLoader().generate()
        enterprise = EnterpriseGenerator(EnterpriseLoader().generate())
        agent = AgentGenerator(EnterpriseLoader().generate())
        contacts = ContactsGenerator(CrmAgentContactsLoader().generate())
        production = ProductionMaker().generate_relate()
        staff = AgentStaffGenerator(staff_info)
        staff_account = AgentStaffAccountGenerator()
        person = PersonMaker(staff_info).generate_relate()
        school = SchoolGenerator(CrmSchoolLoader().generate())
        major = MajorGenerator(CrmMajorLoader().generate())
        goods = GoodsGenerator(goods_info)
        merchandise = MerchandiseMaker(goods_info).generate_relate()
        goods.add_inputs(merchandise, school, major, agent)
        merchandise.add_inputs(production)
        agent.add_outputs(contacts)
        enterprise.add_outputs(agent)
        staff.add_outputs(staff_account)
        staff.add_inputs(enterprise, person)

        return staff
