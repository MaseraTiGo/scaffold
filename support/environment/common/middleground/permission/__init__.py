# coding=UTF-8


from support.common.maker import BaseMaker
from support.common.generator.helper import PlatformGenerator, \
    OrganizationGenerator, PositionGenerator, RuleGenerator, \
    RuleGroupGenerator, AuthorizationGenerator


class PermissionMaker(BaseMaker):
    """
     权限信息初始化
    """
    def __init__(
        self,
        platform_info,
        authorization_info,
        rule_info,
        rule_group_info,
        position_info,
        organization_info
    ):
        self._platform = PlatformGenerator(platform_info)
        self._authorization = AuthorizationGenerator(authorization_info)
        self._rule = RuleGenerator(rule_info)
        self._rule_group = RuleGroupGenerator(rule_group_info)
        self._position = PositionGenerator(position_info)
        self._organization = OrganizationGenerator(organization_info)

    def generate_relate(self):
        self._rule.add_inputs(
            self._platform
        )
        self._authorization.add_inputs(
            self._rule
        )
        self._rule_group.add_inputs(
            self._authorization
        )
        self._position.add_inputs(
            self._rule_group
        )
        self._organization.add_inputs(
            self._position
        )
        return self._platform
