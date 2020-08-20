# coding=UTF-8


from support.common.maker import BaseMaker
# from support.common.generator.helper import BrandGenerator, \
#         ProductionGenerator

from support.common.generator.helper import PlatformGenerator, \
     OrganizationGenerator, PositionGenerator, RuleGroupGenerator, \
     PersonPositionGenerator, AuthorizationGenerator

from support.environment.common.middleground.permission.organization import\
        OrganizationLoader
from support.environment.common.middleground.permission.position import\
        PositionLoader
from support.environment.common.middleground.permission.rulegroup import\
        RuleGroupLoader
from support.environment.common.middleground.permission.platform import\
     PlatformLoader
from support.environment.common.middleground.permission.authorization import\
     AuthorzationLoader

class PermissionMaker(BaseMaker):
    """
     权限信息初始化
    """

    def __init__(self):
        self._platform = PlatformGenerator(
            PlatformLoader().generate()
        )
        self._organization = OrganizationGenerator(
            OrganizationLoader().generate()
        )
        self._position = PositionGenerator(
            PositionLoader().generate()
        )
        self._rule_group = RuleGroupGenerator(
            RuleGroupLoader().generate()
        )
        self._authorization = AuthorizationGenerator(
            AuthorzationLoader().generate()
        )
        self._authorization = AuthorizationGenerator(
            AuthorzationLoader().generate()
        )
        self._person_position = PersonPositionGenerator()
    def generate_relate(self):
        self._position.add_inputs(
            self._organization,
            self._rule_group
        )
        self._authorization.add_outputs(
            self._organization,
            self._position,
            self._rule_group
        )
        self._authorization.add_inputs(
            self._platform
        )
        self._person_position.add_inputs(
            self._authorization,
            self._organization,
            self._position,
        )
        return self._authorization
