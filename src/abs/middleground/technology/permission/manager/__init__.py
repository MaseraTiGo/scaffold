# coding=UTF-8

import json

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.dictwrapper import DictWrapper
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.technology.permission.utils.constant import \
        UseStatus, PermissionTypes
from abs.middleground.technology.permission.models import PlatForm, Rule,\
        RuleGroup, Organization, Position, PositionPermission, PersonGroup, \
        PersonPermission, Authorization
from abs.middleground.technology.permission.manager.rule import \
        RuleHelper
from abs.middleground.technology.permission.manager.register import \
        permission_register


class PermissionServer(BaseManager):

    @classmethod
    def create_platform(cls, name, company_id, app_type, remark, limit=4):
        if PlatForm.query().filter(name=name).count() > 0:
            raise BusinessError("该平台已注册")

        if PlatForm.query(company_id=company_id).count() > limit:
            raise BusinessError("公司授权次数过多")

        platform = PlatForm.create(
            name=name,
            company_id=company_id,
            remark=remark,
            app_type=app_type,
        )
        return platform

    @classmethod
    def get_platform(cls, platform_id):
        platform = PlatForm.get_byid(platform_id)
        if platform is None:
            raise BusinessError("平台不存在")
        return platform

    @classmethod
    def all_platform(cls):
        platform_qs = PlatForm.query()
        return platform_qs

    @classmethod
    def update_platform(cls, platform_id, **update_infos):
        platform = cls.get_platform(platform_id)
        platform.update(**update_infos)
        return platform

    @classmethod
    def authorize(cls, platform_id, company_id, remark):
        platform = cls.get_platform(platform_id)
        authorization = Authorization.create(
            company_id=company_id,
            platform=platform,
            remark=remark,
        )
        return authorization

    @classmethod
    def get_authorization_byappkey(cls, appkey):
        authorization = Authorization.get_byappkey(appkey)
        if authorization is None:
            raise BusinessError("授权不存在")
        return authorization

    @classmethod
    def apply(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        if authorization.use_status != UseStatus.ENABLE:
            authorization.update(
                use_status=UseStatus.ENABLE
            )
        return authorization

    @classmethod
    def forbidden(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        if authorization.use_status != UseStatus.FORBIDDEN:
            authorization.update(
                use_status=UseStatus.FORBIDDEN
            )
        return authorization

    @classmethod
    def refresh(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        authorization.update(
            appkey=authorization.generate_appkey()
        )
        return authorization

    @classmethod
    def get_rule(cls, rule_id):
        rule = Rule.get_byid(rule_id)
        if rule is None:
            raise BusinessError("规则没有配置")
        return rule

    @classmethod
    def get_all_rule_byplatform(cls, platform_id):
        platform = cls.get_platform(platform_id)
        return RuleHelper(platform).root.get_tree()

    @classmethod
    def add_rule(cls, platform_id, name, parent_id, description, remark):
        platform = cls.get_platform(platform_id)
        rule = Rule.create(
            name=name,
            description=description,
            remark=remark,
            parent_id=parent_id,
            platform=platform,
        )
        return rule

    @classmethod
    def update_rule(cls, rule_id, **update_info):
        rule = cls.get_rule(rule_id)
        rule.update(**update_info)
        return rule

    @classmethod
    def remove_rule(cls, rule_id):
        return cls.get_rule(rule_id).delete()

    @classmethod
    def get_organization(cls, organization_id):
        organization = Organization.get_byid(organization_id)
        if organization is None:
            raise BusinessError("组织不存在")
        return organization

    @classmethod
    def get_all_organization_byappkey(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        helper = permission_register.get_helper(authorization).organization
        all_organization = []
        if helper.root is not None:
            all_organization = helper.root.get_tree()
        return all_organization

    @classmethod
    def add_organization(cls, appkey, parent_id, name, description, remark):
        authorization = cls.get_authorization_byappkey(appkey)
        organization = Organization.create(
            name=name,
            parent_id=parent_id,
            description=description,
            remark=remark,
            authorization=authorization,
        )
        permission_register.get_helper(
            authorization
        ).organization.force_refresh()
        return organization

    @classmethod
    def update_organization(cls, organization_id, **update_info):
        organization = cls.get_organization(organization_id)
        organization.update(**update_info)
        permission_register.get_helper(
            organization.authorization
        ).organization.force_refresh()
        return organization

    @classmethod
    def remove_organization(cls, organization_id):
        organization = cls.get_organization(organization_id)
        organization.delete()
        permission_register.get_helper(
            organization.authorization
        ).organization.force_refresh()
        return True

    @classmethod
    def get_rule_group(cls, rule_group_id):
        rule_group = RuleGroup.get_byid(rule_group_id)
        if rule_group is None:
            raise BusinessError("权限组没有配置")
        return rule_group

    @classmethod
    def search_rule_group(cls, current_page, appkey, **search_info):
        authorization = cls.get_authorization_byappkey(appkey)
        rule_group_qs = RuleGroup.query(
            authorization=authorization
        ).filter(**search_info)
        spliter = Splitor(current_page, rule_group_qs)
        return spliter

    @classmethod
    def add_rule_group(cls, appkey, name, description, remark, content):
        authorization = cls.get_authorization_byappkey(appkey)
        rule_group = RuleGroup.create(
            name=name,
            description=description,
            remark=remark,
            content=content,
            authorization=authorization,
        )
        return rule_group

    @classmethod
    def update_rule_group(cls, rule_group_id, **update_info):
        rule_group = cls.get_rule_group(rule_group_id)
        rule_group.update(**update_info)
        return rule_group

    @classmethod
    def remove_rule_group(cls, rule_group_id):
        return cls.get_rule_group(rule_group_id).delete()

    @classmethod
    def get_position(cls, position_id):
        position = Position.get_byid(position_id)
        if position is None:
            raise BusinessError("身份不存在")
        return position

    @classmethod
    def get_all_position_byappkey(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        helper = permission_register.get_helper(authorization).position
        all_position = []
        if helper.root is not None:
            all_position = helper.root.get_tree()
        return all_position

    @classmethod
    def add_position(
        cls,
        appkey,
        organization_id,
        rule_group_id,
        parent_id,
        name,
        description,
        remark
    ):
        authorization = cls.get_authorization_byappkey(appkey)
        organization = cls.get_organization(organization_id)
        rule_group = cls.get_rule_group(rule_group_id)
        position = Position.create(
            name=name,
            description=description,
            parent_id=parent_id,
            remark=remark,
            organization=organization,
            rule_group=rule_group,
            authorization=authorization,
        )
        permission_register.get_helper(authorization).position.force_refresh()
        return position

    @classmethod
    def update_position(cls, position_id, **update_info):
        position = cls.get_position(position_id)
        position.update(**update_info)
        permission_register.get_helper(
            position.authorization
        ).position.force_refresh()
        return position

    @classmethod
    def remove_position(cls, position_id):
        position = cls.get_position(position_id)
        position.delete()
        permission_register.get_helper(
            position.authorization
        ).position.force_refresh()
        return True

    @classmethod
    def get_person_group(cls, person_group_id):
        person_group = PersonGroup.get_byid(person_group_id)
        if person_group is None:
            raise BusinessError("用户组不存在")
        return person_group

    @classmethod
    def add_person_group(
        cls,
        appkey,
        rule_group_id,
        name,
        description,
        remark
    ):
        authorization = cls.get_authorization_byappkey(appkey)
        rule_group = cls.get_rule_group(rule_group_id)
        person_group = PersonGroup.create(
            name=name,
            description=description,
            remark=remark,
            rule_group=rule_group,
            authorization=authorization,
        )
        return person_group

    @classmethod
    def update_person_group(cls, person_group_id, **update_info):
        person_group = cls.get_person_group(person_group_id)
        person_group.update(**update_info)
        return person_group

    @classmethod
    def remove_person_group(cls, person_group_id):
        return cls.get_person_group(person_group_id).delete()

    @classmethod
    def bind_position(cls, appkey, organization_id, position_id, person_id):
        authorization = cls.get_authorization_byappkey(appkey)
        organization = cls.get_organization(organization_id)
        position = cls.get_position(position_id)
        permission = PositionPermission.create(
            person_id=person_id,
            organization=organization,
            position=position,
            authorization=authorization,
        )
        return permission

    @classmethod
    def get_position_permission(cls, appkey, person_id):
        authorization = cls.get_authorization_byappkey(appkey)
        position_permission = PositionPermission.get_byposition(
            authorization=authorization,
            person_id=person_id,
        )

        helper = permission_register.get_helper(authorization)
        organization_id_list = helper.organization.get_children_ids(
            position_permission.organization.id
        )
        position_id_list = helper.position.get_children_ids(
            position_permission.position.id
        )
        person_id_list = [
            permission['person_id']
            for permission in PositionPermission.query().filter(
                organization_id__in=organization_id_list,
                position_id__in=position_id_list,
                authorization=authorization,
            ).values('person_id')
        ]

        permission = DictWrapper({
            'operation': json.loads(
                position_permission.position.rule_group.content
            ),
            'data': [
                person_id_list
            ],
        })
        return permission

    @classmethod
    def bind_person(cls, appkey, person_group_id, person_id):
        authorization = cls.get_authorization_byappkey(appkey)
        person_group = cls.get_person_group(person_group_id)
        permission = PersonPermission.creaet(
            person_id=person_id,
            person_group=person_group,
            authorization=authorization,
        )
        return permission

    @classmethod
    def get_person_permission(cls, appkey, person_id):
        authorization = cls.get_authorization_byappkey(appkey)
        person_permission = PersonPermission.get_byperson(
            authorization=authorization,
            person_id=person_id
        )
        if person_permission is None:
            raise BusinessError("个人权限不存在")
        permission = DictWrapper({
            'operation': json.loads(
                person_permission.person_group.rule_group.content
            ),
            'data': [
                person_id
            ],
        })
        return permission

    @classmethod
    def get_permission(cls, appkey, person_id):
        """
        return :
            {
                operation:[
                    {
                        name: xxxx
                        code: A
                        children: [
                            {
                                name: xxxx
                                code: A
                                children: {}
                            },
                            .....
                        ]
                    },
                    .....
                ],
                data:[
                    persion_id,
                    .....
                ]

            }
        """
        authorization = cls.get_authorization_byappkey(appkey)
        if authorization.platform.app_type == PermissionTypes.POSITION:
            return cls.get_position_permission(appkey, person_id)
        if authorization.platform.app_type == PermissionTypes.PERSON:
            return cls.get_person_permission(appkey, person_id)
        raise BusinessError("权限类型不支持")
