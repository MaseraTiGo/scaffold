# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import EnterpriseGenerator, \
        StaffGenerator, StaffAccountGenerator, SpaceGenerator, ParamGenerator
from support.environment.common.middleground.person import PersonMaker
from support.environment.common.middleground.production import ProductionMaker
from support.environment.common.middleground.permission import PermissionMaker
from support.environment.common.business.crm.years import YearsMaker
from support.environment.init.business.crm.enterprise import EnterpriseLoader
from support.environment.init.business.crm.staff import StaffLoader
from support.environment.init.business.crm.school import SchoolLoader
from support.environment.init.business.crm.major import MajorLoader
from support.environment.init.business.crm.relations import RelationsLoader
from support.environment.init.business.crm.space import SpaceLoader
from support.environment.init.business.crm.param import ParamLoader
from support.environment.init.business.crm.platform import \
        PlatformLoader
from support.environment.init.business.crm.authorization import \
        AuthorizationLoader
from support.environment.init.business.crm.rule import RuleLoader
from support.environment.init.business.crm.rulegroup import \
        RuleGroupLoader
from support.environment.init.business.crm.position import \
        PositionLoader
from support.environment.init.business.crm.organization import \
        OrganizationLoader

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
        self._permission = PermissionMaker(
            PlatformLoader().generate(),
            AuthorizationLoader().generate(),
            RuleLoader().generate(),
            RuleGroupLoader().generate(),
            PositionLoader().generate(),
            OrganizationLoader().generate(),
        ).generate_relate()
        self._person = PersonMaker(StaffLoader().generate()).generate_relate()
        self._production = ProductionMaker().generate_relate()
        self._enterprise = EnterpriseGenerator(EnterpriseLoader().generate())
        self._staff = StaffGenerator(StaffLoader().generate())
        self._staff_account = StaffAccountGenerator()
        years = YearsMaker(
            SchoolLoader().generate(),
            MajorLoader().generate(),
            RelationsLoader().generate(),
            RelationsLoader().generate()
        ).generate_relate().generate()
        self._space = SpaceGenerator(SpaceLoader().generate()).generate()
        self._param = ParamGenerator(ParamLoader().generate()).generate()


    def generate_relate(self):
        self._enterprise.add_outputs(self._production)
        self._permission.add_inputs(self._enterprise)
        self._staff.add_outputs(self._staff_account)
        self._staff.add_inputs(self._permission, self._person)

        return self._staff


if __name__ == "__main__":
    CrmInitializeMaker().run()
