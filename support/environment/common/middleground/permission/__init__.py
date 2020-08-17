# coding=UTF-8


from support.common.maker import BaseMaker
# from support.common.generator.helper import BrandGenerator, \
#         ProductionGenerator

from support.common.generator.helper import PlatformGenerator, \
     OrganizationGenerator, PositionGenerator, RuleGroupGenerator

from support.environment.common.middleground.permission.organization import\
        OrganizationLoader
from support.environment.common.middleground.permission.position import\
        PositionLoader
from support.environment.common.middleground.permission.rulegroup import\
        RuleGroupLoader

class PermissionMaker(BaseMaker):
    """
     权限信息初始化
    """

    def __init__(self):
        self._platform = PlatformGenerator()
        self._organization = OrganizationGenerator(
            OrganizationLoader().generate()
        )
        self._position = PositionGenerator(
            PositionLoader().generate()
        )
        self._rule_group = RuleGroupGenerator(
            RuleGroupLoader().generate()
        )
    def generate_relate(self):
        self._position.add_inputs(
            self._organization,
            self._rule_group
        )
        self._platform.add_outputs(
            self._organization,
            self._position,
            self._rule_group
        )
        return self._platform
