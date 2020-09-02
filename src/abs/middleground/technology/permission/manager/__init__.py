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
    def create_platform(
        cls,
        name,
        company_id,
        company_name,
        app_type,
        remark,
        limit=100
    ):
        if PlatForm.query().filter(name=name).count() > 0:
            raise BusinessError("该平台已注册")

        if PlatForm.query(company_id=company_id).count() > limit:
            raise BusinessError("公司授权次数过多")

        platform = PlatForm.create(
            name=name,
            company_id=company_id,
            company_name=company_name,
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
    def search_platform(cls, current_page, **search_info):
        platform_qs = PlatForm.query(
            **search_info
        ).order_by("-create_time")
        spliter = Splitor(current_page, platform_qs)
        return spliter

    @classmethod
    def update_platform(cls, platform_id, **update_infos):
        platform = cls.get_platform(platform_id)
        platform.update(**update_infos)
        return platform

    @classmethod
    def remove_platform(cls, platform_id):
        platform = cls.get_platform(platform_id)
        authorization_list = Authorization.get_byplatform(platform)
        if authorization_list:
            raise BusinessError("该平台已有公司被授权，不可删除")
        platform.delete()

    @classmethod
    def get_authorization(cls, authorization_id):
        authorization = Authorization.get_byid(authorization_id)
        if authorization is None:
            raise BusinessError("授权不存在")
        return authorization

    @classmethod
    def get_authorization_byappkey(cls, appkey):
        authorization = Authorization.get_byappkey(appkey)
        if authorization is None:
            raise BusinessError("授权不存在")
        return authorization

    @classmethod
    def search_authorization(cls, current_page, platform_id, **search_info):
        platform = cls.get_platform(platform_id)
        authorization_qs = Authorization.query(
            platform=platform,
            **search_info
        ).filter(
        )
        spliter = Splitor(current_page, authorization_qs)
        return spliter

    @classmethod
    def update_authorization(cls, authorization_id, **update_info):
        authorization = cls.get_authorization(authorization_id)
        authorization.update(
            **update_info
        )

    @classmethod
    def remove_authorization(cls, authorization_id):
        authorization = cls.get_authorization(authorization_id)
        authorization.delete()

    @classmethod
    def authorize(cls, platform_id, company_id, company_name, remark):
        platform = cls.get_platform(platform_id)
        is_exsited = Authorization.check_unique(
            platform_id,
            company_id
        )
        if is_exsited:
            raise BusinessError("该公司重复授权")

        authorization = Authorization.create(
            company_id=company_id,
            company_name=company_name,
            platform=platform,
            remark=remark,
        )
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
        all_rule = [
            entity.get_tree()
            for entity in RuleHelper(platform).root.get_children()
        ]
        return all_rule

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
        rule = cls.get_rule(rule_id)
        if rule.get_children():
            raise BusinessError("不能删除，规则下面仍有子节点!")
        rule.delete()

    @classmethod
    def add_organization(
        cls,
        appkey,
        position_id_list,
        parent_id,
        name,
        description,
        remark
    ):
        authorization = cls.get_authorization_byappkey(appkey)
        organization = Organization.create(
            name=name,
            parent_id=parent_id,
            description=description,
            position_id_list=json.dumps(position_id_list),
            remark=remark,
            authorization=authorization,
        )
        permission_register.get_helper(
            authorization
        ).organization.force_refresh()
        return organization

    @classmethod
    def _hung_position_byorganization(cls, organization_list):
        position_id_set = set()
        for organization in organization_list:
            for position_id in json.loads(organization.position_id_list):
                position_id_set.add(position_id)

        position_map = {
            position.id: position
            for position in Position.search(
                id__in=list(position_id_set)
            )
        }

        for organization in organization_list:
            position_list = []
            for position_id in json.loads(organization.position_id_list):
                position_list.append(
                    position_map[position_id]
                )
            organization.position_list = position_list

    @classmethod
    def get_organization(cls, organization_id):
        organization = Organization.get_byid(organization_id)
        if organization is None:
            raise BusinessError("组织不存在")
        cls._hung_position_byorganization([organization])
        return organization

    @classmethod
    def search_organization_byappkey(cls, appkey, current_page, **search_info):
        authorization = cls.get_authorization_byappkey(appkey)
        organization_qs = Organization.query(
            authorization=authorization,
            **search_info
        )
        spliter = Splitor(current_page, organization_qs)
        cls._hung_position_byorganization(spliter.get_list())
        return spliter

    @classmethod
    def get_all_organization_byappkey(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        helper = permission_register.get_helper(authorization).organization
        all_organization = [
            entity
            for entity in helper.get_all_list()
        ]
        return all_organization

    @classmethod
    def get_tree_organization_byappkey(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        helper = permission_register.get_helper(authorization).organization
        all_organization = [
            entity.get_tree()
            for entity in helper.root.get_children()
        ]
        return all_organization

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
    def all_rule_group(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        rule_group_qs = RuleGroup.query(
            authorization=authorization,
        ).filter()
        return rule_group_qs

    @classmethod
    def search_rule_group(cls, current_page, appkey, **search_info):
        authorization = cls.get_authorization_byappkey(appkey)
        rule_group_qs = RuleGroup.query(
            authorization=authorization,
            **search_info
        ).filter()
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
    def search_position_byappkey(cls, appkey, current_page, **search_info):
        authorization = cls.get_authorization_byappkey(appkey)
        position_qs = Position.query(
            authorization=authorization,
            **search_info
        )
        spliter = Splitor(current_page, position_qs)
        return spliter

    @classmethod
    def get_all_position_byappkey(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        helper = permission_register.get_helper(authorization).position
        all_position = [
            entity
            for entity in helper.get_all_list()
        ]
        return all_position

    @classmethod
    def get_tree_position_byappkey(cls, appkey):
        authorization = cls.get_authorization_byappkey(appkey)
        helper = permission_register.get_helper(authorization).position
        all_position = [
            entity.get_tree()
            for entity in helper.root.get_children()
        ]
        return all_position

    @classmethod
    def add_position(
        cls,
        appkey,
        rule_group_id,
        parent_id,
        name,
        description,
        remark
    ):
        authorization = cls.get_authorization_byappkey(appkey)
        rule_group = cls.get_rule_group(rule_group_id)
        position = Position.create(
            name=name,
            description=description,
            parent_id=parent_id,
            remark=remark,
            rule_group=rule_group,
            authorization=authorization,
        )
        permission_register.get_helper(authorization).position.force_refresh()
        return position

    @classmethod
    def update_position(cls, position_id, **update_info):
        position = cls.get_position(position_id)
        if "rule_group_id" in update_info:
            rule_group_id = update_info.pop("rule_group_id")
            rule_group = cls.get_rule_group(rule_group_id)
            update_info.update({"rule_group": rule_group})
        position.update(**update_info)
        permission_register.get_helper(
            position.authorization
        ).position.force_refresh()
        return position

    @classmethod
    def remove_position(cls, position_id):
        position = cls.get_position(position_id)
        position_qs = position.get_children()
        if position_qs.count() > 0:
            raise BusinessError("身份存有下级节点，不能删除")
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
        organization_id_list = helper.organization.get_all_children_ids(
            position_permission.organization.id
        )
        organization_id_list.append(position_permission.organization.id)
        position_id_list = helper.position.get_all_children_ids(
            position_permission.position.id
        )
        position_id_list.append(position_permission.position.id)
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
