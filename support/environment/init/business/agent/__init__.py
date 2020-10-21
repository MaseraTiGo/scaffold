# coding=UTF-8


from support.common.generator.helper import EnterpriseGenerator
from support.common.generator.helper.business.agent.account import AgentStaffAccountGenerator
from support.common.generator.helper.business.agent.contacts import ContactsGenerator
from support.common.generator.helper.business.agent.staff import AgentStaffGenerator
from support.common.generator.helper.business.agent.template import TemplateGenerator
from support.common.generator.helper.business.agent.template_param import TemplateParamGenerator
from support.common.generator.helper.business.agent.goods import GoodsGenerator
from support.common.generator.helper.business.agent.goods.review import GoodsReviewGenerator

from support.common.generator.helper.business.crm.agent import AgentGenerator
from support.common.maker import BaseMaker
from support.environment.common.middleground.permission import PermissionMaker
from support.environment.common.middleground.production import ProductionMaker
from support.environment.init.business.agent.contact import ContactLoader
from support.environment.init.business.agent.enterprise import AgentLoader
from support.environment.init.business.agent.staff import AgentStaffLoader
from support.environment.init.business.agent.template import TemplateLoader
from support.environment.init.business.agent.template import TemplateParamLoder
from support.environment.init.business.agent.merchandise import MerchandiseLoader
from support.environment.init.business.agent.goods import GoodsLoader
from support.environment.init.business.agent.authorization import AuthorizationLoader
from support.environment.init.business.agent.organization import OrganizationLoader
from support.environment.init.business.agent.platform import PlatformLoader
from support.environment.init.business.agent.position import PositionLoader
from support.environment.init.business.agent.rule import RuleLoader
from support.environment.init.business.agent.rulegroup import RuleGroupLoader
from support.environment.common.middleground.person import PersonMaker
from support.environment.common.middleground.merchandise import MerchandiseMaker
from support.environment.init.business.crm.school import SchoolLoader
from support.environment.init.business.crm.major import MajorLoader
from support.environment.init.business.crm.relations import RelationsLoader
from support.environment.common.business.crm.years import YearsMaker
from support.environment.init.business.agent.customer import CustomerLoader
from support.common.generator.helper.business.agent.customer import CustomerGenerator
from support.environment.init.business.agent.customer.order import CustomerOrderLoader
# from support.common.generator.helper.business.agent.customer.order import OrderGenerator
from support.common.generator.helper.business.agent.persongroup import PersonGroupGenerator
from support.common.generator.helper.business.agent.personpermission import PersonPermissionGenerator
from support.environment.init.business.agent.persongroup import PersonGroupLoader


class AgentInitializeMaker(BaseMaker):
    """
    仅仅管理agent初始化的数据
    1、企业数据
    2、部门数据
    3、角色数据
    4、员工及员工账号数据
    6、商品数据
    7、合同模板
    8、商品列表
    """

    def __init__(self):
        self._permission = PermissionMaker(
            PlatformLoader().generate(),
            AuthorizationLoader().generate(),
            RuleLoader().generate(),
            RuleGroupLoader().generate(),
            PositionLoader().generate(),
            OrganizationLoader().generate(),
        ).generate_relate()
        self._person = PersonMaker(AgentStaffLoader().generate()).generate_relate()
        self._production = ProductionMaker().generate_relate()
        self._enterprise = EnterpriseGenerator(AgentLoader().generate())
        self._agent_base = AgentGenerator(AgentLoader().generate())
        self._contacts = ContactsGenerator(ContactLoader().generate())
        self._agent_staff = AgentStaffGenerator(AgentStaffLoader().generate())
        self._agent_staff_account = AgentStaffAccountGenerator()
        self._template = TemplateGenerator(TemplateLoader().generate())
        self._template_param = TemplateParamGenerator(TemplateParamLoder().generate())
        self._merchandise = MerchandiseMaker(MerchandiseLoader().generate()).generate_relate()
        self._years = YearsMaker(SchoolLoader().generate(), MajorLoader().generate(), RelationsLoader().generate(),
                   RelationsLoader().generate()).generate_relate()
        self._goods = GoodsGenerator(GoodsLoader().generate())
        self._goods_review = GoodsReviewGenerator()
        self._agent_customer = CustomerGenerator(CustomerLoader().generate())
        # self._order = OrderGenerator(CustomerOrderLoader().generate())
        self._person_group = PersonGroupGenerator(PersonGroupLoader().generate())
        self._person_permission = PersonPermissionGenerator(AgentStaffLoader().generate())

    def generate_relate(self):
        self._enterprise.add_outputs(self._production)
        self._permission.add_inputs(self._enterprise)
        self._agent_staff.add_outputs(self._agent_staff_account)
        self._agent_staff.add_inputs(self._permission, self._person, self._agent_base)
        self._template.add_inputs(self._agent_base)
        self._template.add_outputs(self._template_param)
        self._agent_staff_account.add_outputs(self._goods)
        self._goods.add_inputs(self._template, self._merchandise, self._years)
        self._goods_review.add_inputs(self._goods)
        self._agent_customer.add_inputs(self._person, self._agent_base)
        # self._agent_customer.add_outputs(self._order)
        self._person_group.add_inputs(self._agent_staff_account)
        self._person_permission.add_inputs(self._person_group)
        self._contacts.add_inputs(self._agent_base)
        return self._agent_staff


if __name__ == "__main__":
    AgentInitializeMaker().run()
