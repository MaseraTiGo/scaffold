# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import EnterpriseGenerator,\
        ControllerStaffGenerator, ControllerStaffAccountGenerator
from support.environment.common.middleground.person import PersonMaker
from support.environment.common.middleground.permission import PermissionMaker
# from support.environment.common.middleground.production import \
#         ProductionMaker
from support.environment.init.business.controller.enterprise import \
        EnterpriseLoader
from support.environment.init.business.controller.platform import \
        PlatformLoader
from support.environment.init.business.controller.rule import RuleLoader
from support.environment.init.business.controller.authorization import \
        AuthorizationLoader
from support.environment.init.business.controller.rulegroup import \
        RuleGroupLoader
from support.environment.init.business.controller.position import \
        PositionLoader
from support.environment.init.business.controller.organization import \
        OrganizationLoader
from support.environment.init.business.controller.staff import StaffLoader


class ControllerInitializeMaker(BaseMaker):
    """
    仅仅管理crm初始化的数据
    1、企业数据
    2、平台数据
    3、授权数据
    4、组织数据
    5、职位数据
    6、员工及员工账号数据
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
        self._person = PersonMaker(
            StaffLoader().generate()
        ).generate_relate()
        self._enterprise = EnterpriseGenerator(
            EnterpriseLoader().generate()
        )
        self._staff = ControllerStaffGenerator(
            StaffLoader().generate()
        )
        self._staff_account = ControllerStaffAccountGenerator()

    def generate_relate(self):
        self._permission.add_inputs(self._enterprise)
        self._staff.add_inputs(self._permission, self._person)
        self._staff.add_outputs(self._staff_account)
        return self._enterprise


if __name__ == "__main__":
    ControllerInitializeMaker().run()
