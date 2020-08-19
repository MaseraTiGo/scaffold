# coding=UTF-8

import json

from abs.middleground.technology.permission.utils.constant import\
        PermissionTypes
from support.common.testcase.controller_api_test_case import \
        ControllerAPITestCase
from support.common.generator.field.model.entity import CrnCompanyEntitry,\
        CustomerEntity, CrnStaffEntitry


class PermissionTestCase(ControllerAPITestCase):

    def setUp(self):
        self.company = CrnCompanyEntitry().generate()
        self.staff = CrnStaffEntitry().generate()
        self.customer = CustomerEntity().generate()

    def tearDown(self):
        pass

    def assert_position_fields(self, position):
        self.assertTrue('id' in position)
        self.assertTrue('name' in position)
        self.assertTrue('parent_id' in position)
        self.assertTrue('organization_id' in position)
        self.assertTrue('rule_group_id' in position)
        self.assertTrue('description' in position)
        self.assertTrue('remark' in position)
        self.assertTrue('create_time' in position)

    def assert_rulegroup_fields(self, rule_group):
        self.assertTrue('id' in rule_group)
        self.assertTrue('name' in rule_group)
        self.assertTrue('content' in rule_group)
        self.assertTrue('description' in rule_group)
        self.assertTrue('remark' in rule_group)
        self.assertTrue('create_time' in rule_group)
        self.assertTrue('update_time' in rule_group)

    def assert_rule_fields(self, rule, is_all=False):
        if is_all:
            self.assertTrue('id' in rule)
            self.assertTrue('parent_id' in rule)
            self.assertTrue('remark' in rule)
            self.assertTrue('create_time' in rule)
        self.assertTrue('name' in rule)
        self.assertTrue('code' in rule)

    def assert_organization_fields(self, organization):
        self.assertTrue('id' in organization)
        self.assertTrue('name' in organization)
        self.assertTrue('parent_id' in organization)
        self.assertTrue('remark' in organization)
        self.assertTrue('description' in organization)
        self.assertTrue('create_time' in organization)

    def assert_platform_fields(self, platform):
        self.assertTrue('id' in platform)
        self.assertTrue('name' in platform)
        self.assertTrue('company_id' in platform)
        self.assertTrue('remark' in platform)

    def platform_add(self):
        api = 'staff.permission.platform.add'
        result = self.access_api(
            api=api,
            authorize_info=json.dumps({
                'name': "必圈CRM平台",
                'company_id': self.company.id,
                'app_type': PermissionTypes.POSITION,
                'remark': '必圈公司',
            })
        )
        self.assertTrue('platform_id' in result)
        return result['platform_id']

    def platform_update(self, platform_id):
        api = 'staff.permission.platform.update'
        self.access_api(
            api=api,
            platform_id=platform_id,
            update_info=json.dumps({
                'name': "必圈CRM平台-更新",
                'remark': '必圈公司-更新',
            })
        )

    def platform_all(self):
        api = 'staff.permission.platform.all'
        result = self.access_api(
            api=api,
        )
        self.assertTrue('data_list' in result)
        for platform in result['data_list']:
            self.assert_platform_fields(platform)

    def platform_authorize(self, platform_id):
        api = 'staff.permission.platform.authorize'
        result = self.access_api(
            api=api,
            platform_id=platform_id,
            authorize_info=json.dumps({
                'company_id': self.company.id,
                'remark': '必圈公司授权',
            })
        )
        self.assertTrue('appkey' in result)
        return result['appkey']

    def platform_apply(self, appkey):
        api = 'staff.permission.platform.apply'
        self.access_api(
            api=api,
            appkey=appkey,
        )

    def platform_forbidden(self, appkey):
        api = 'staff.permission.platform.forbidden'
        self.access_api(
            api=api,
            appkey=appkey,
        )

    def platform_refresh(self, appkey):
        api = 'staff.permission.platform.refresh'
        result = self.access_api(
            api=api,
            appkey=appkey,
        )
        self.assertTrue('appkey' in result)
        return result['appkey']

    def rule_add(self, platform_id, **rule_info):
        api = 'staff.permission.rule.add'
        result = self.access_api(
            api=api,
            platform_id=platform_id,
            rule_info=json.dumps(rule_info)
        )
        self.assertTrue('rule_id' in result)
        return result['rule_id']

    def rule_get(self, rule_id):
        api = 'staff.permission.rule.get'
        result = self.access_api(
            api=api,
            rule_id=rule_id
        )
        self.assertTrue('rule_info' in result)
        self.assert_rule_fields(result['rule_info'], True)
        return result['rule_info']

    def rule_update(self, rule_id, **update_info):
        api = 'staff.permission.rule.update'
        self.access_api(
            api=api,
            rule_id=rule_id,
            update_info=json.dumps(update_info)
        )

    def rule_remove(self, rule_id, **update_info):
        api = 'staff.permission.rule.remove'
        self.access_api(
            api=api,
            rule_id=rule_id,
        )

    def rule_all(self, platform_id):
        api = 'staff.permission.rule.all'
        result = self.access_api(
            api=api,
            platform_id=platform_id,
        )
        self.assertTrue('rule_list' in result)
        for rule in result['rule_list']:
            self.assert_rule_fields(rule)
        return result['rule_list']

    def organization_add(self, appkey, **organization_info):
        api = 'staff.permission.organization.add'
        result = self.access_api(
            api=api,
            appkey=appkey,
            organization_info=json.dumps(organization_info)
        )
        self.assertTrue('organization_id' in result)
        return result['organization_id']

    def organization_get(self, organization_id):
        api = 'staff.permission.organization.get'
        result = self.access_api(
            api=api,
            organization_id=organization_id
        )
        self.assertTrue('organization_info' in result)
        self.assert_organization_fields(result['organization_info'], True)
        return result['organization_info']

    def organization_update(self, organization_id, **update_info):
        api = 'staff.permission.organization.update'
        self.access_api(
            api=api,
            organization_id=organization_id,
            update_info=json.dumps(update_info)
        )

    def organization_remove(self, organization_id, **update_info):
        api = 'staff.permission.organization.remove'
        self.access_api(
            api=api,
            organization_id=organization_id,
        )

    def organization_all(self, appkey):
        api = 'staff.permission.organization.all'
        result = self.access_api(
            api=api,
            appkey=appkey,
        )
        self.assertTrue('organization_list' in result)
        for organization in result['organization_list']:
            self.assert_organization_fields(organization)
        return result['organization_list']

    def position_add(self, appkey, **position_info):
        api = 'staff.permission.position.add'
        result = self.access_api(
            api=api,
            appkey=appkey,
            position_info=json.dumps(position_info)
        )
        self.assertTrue('position_id' in result)
        return result['position_id']

    def position_get(self, position_id):
        api = 'staff.permission.position.get'
        result = self.access_api(
            api=api,
            position_id=position_id
        )
        self.assertTrue('position_info' in result)
        self.assert_position_fields(result['position_info'])
        return result['position_info']

    def position_update(self, position_id, **update_info):
        api = 'staff.permission.position.update'
        self.access_api(
            api=api,
            position_id=position_id,
            update_info=json.dumps(update_info)
        )

    def position_remove(self, position_id, **update_info):
        api = 'staff.permission.position.remove'
        self.access_api(
            api=api,
            position_id=position_id,
        )

    def position_all(self, appkey):
        api = 'staff.permission.position.all'
        result = self.access_api(
            api=api,
            appkey=appkey,
        )
        self.assertTrue('position_list' in result)
        for position in result['position_list']:
            self.assert_position_fields(position)
        return result['position_list']

    def rulegroup_add(self, appkey, **rule_group_info):
        api = 'staff.permission.rulegroup.add'
        result = self.access_api(
            api=api,
            appkey=appkey,
            rule_group_info=json.dumps(rule_group_info)
        )
        self.assertTrue('rule_group_id' in result)
        return result['rule_group_id']

    def rulegroup_get(self, rule_group_id):
        api = 'staff.permission.rulegroup.get'
        result = self.access_api(
            api=api,
            rule_group_id=rule_group_id
        )
        self.assertTrue('rule_group_info' in result)
        self.assert_rulegroup_fields(result['rule_group_info'])
        return result['rule_group_info']

    def rulegroup_update(self, rule_group_id, **update_info):
        api = 'staff.permission.rulegroup.update'
        self.access_api(
            api=api,
            rule_group_id=rule_group_id,
            update_info=json.dumps(update_info)
        )

    def rulegroup_remove(self, rule_group_id, **update_info):
        api = 'staff.permission.rulegroup.remove'
        self.access_api(
            api=api,
            rule_group_id=rule_group_id,
        )

    def rulegroup_search(self, appkey, current_page, **search_info):
        api = 'staff.permission.rulegroup.search'
        result = self.access_api(
            api=api,
            appkey=appkey,
            current_page=current_page,
            search_info=json.dumps(search_info),
        )
        self.assertTrue('total' in result)
        self.assertTrue('total_page' in result)
        self.assertTrue('data_list' in result)
        for rule_group in result['data_list']:
            self.assert_rulegroup_fields(rule_group)
        return result['data_list']

    def bind_position(
        self,
        appkey,
        organization_id,
        position_id,
        person_id
    ):
        api = 'staff.permission.bind.position'
        self.access_api(
            api=api,
            appkey=appkey,
            bind_info=json.dumps({
                'organization_id': organization_id,
                'position_id': position_id,
                'person_id': person_id,
            })
        )

    def get_permission(self, appkey, person_id):
        api = 'staff.permission.get'
        result = self.access_api(
            api=api,
            appkey=appkey,
            person_id=person_id,
        )
        self.assertTrue('operation' in result)
        self.assertTrue('data' in result)

    def test_permission_workflow(self):
        # 1. 创建平台
        platform_id = self.platform_add()
        self.platform_update(platform_id)
        self.platform_all()
        appkey = self.platform_authorize(platform_id)

        # 2. 启动授权
        self.platform_apply(appkey)
        self.platform_forbidden(appkey)
        appkey = self.platform_refresh(appkey)
        self.platform_apply(appkey)

        # 3. 测试规则
        rule_id = self.rule_add(
            platform_id,
            name="权限管理",
            parent_id=0,
            description="一级权限描述",
            remark="一级权限",
        )
        rule_id_2 = self.rule_add(
            platform_id,
            name="权限列表",
            parent_id=rule_id,
            description="二级权限描述",
            remark="二级权限",
        )
        rule_id_3 = self.rule_add(
            platform_id,
            name="查看",
            parent_id=rule_id_2,
            description="查看操作描述",
            remark="查看操作权限",
        )
        rule_id_3 = self.rule_add(
            platform_id,
            name="详情",
            parent_id=rule_id_2,
            description="查看操作描述",
            remark="查看操作权限",
        )
        rule_id_2 = self.rule_add(
            platform_id,
            name="组织列表",
            parent_id=rule_id,
            description="组织列表描述",
            remark="组织列表权限",
        )
        rule_id_3 = self.rule_add(
            platform_id,
            name="详情",
            parent_id=rule_id_2,
            description="详情操作描述",
            remark="详情操作权限",
        )
        self.rule_update(rule_id_3, name='删除', remark="删除操作备注")
        self.rule_all(platform_id)
        self.rule_remove(rule_id_3)

        # 4.测试权限组
        rule_group_id = self.rulegroup_add(
            appkey,
            name="管理员权限",
            description="一级权限描述",
            remark="一级权限",
            content=json.dumps([
                'WRNA-UwQa-rTUx',
                'WRNA-UwQa-HOTn',
                'WRNA-UORI-HOTn',
            ])
        )
        rule_group_id_2 = self.rulegroup_add(
            appkey,
            name="临时员权限",
            description="一级权限描述",
            remark="一级权限",
            content=json.dumps([
                'WRNA-UwQa-rTUx',
            ])
        )
        self.rulegroup_update(
            rule_group_id_2,
            name='其他权限',
            remark="其他角色权限"
        )
        self.rulegroup_search(
            appkey,
            current_page=1
        )
        self.rulegroup_remove(rule_group_id_2)

        # 5. 测试组织
        organization_id = self.organization_add(
            appkey,
            name="公司",
            parent_id=0,
            description="公司描述",
            remark="公司备注",
        )
        organization_id_2 = self.organization_add(
            appkey,
            name="研发部",
            parent_id=organization_id,
            description="研发部二级权限描述",
            remark="研发部二级权限",
        )
        organization_id_3 = self.organization_add(
            appkey,
            name="项目一组",
            parent_id=organization_id_2,
            description="项目一组查看操作描述",
            remark="项目一组查看操作权限",
        )
        organization_id_3 = self.organization_add(
            appkey,
            name="项目2组",
            parent_id=organization_id_2,
            description="项目2组查看操作描述",
            remark="项目2组查看操作权限",
        )
        organization_id_2 = self.organization_add(
            appkey,
            name="增值部",
            parent_id=organization_id,
            description="增值部组织列表描述",
            remark="增值部组织列表权限",
        )
        self.organization_update(
            organization_id_3,
            name='项目二部',
            remark="项目二部备注",
            description="项目二部描述"
        )
        self.organization_all(appkey)
        self.organization_remove(organization_id_3)

        position_id = self.position_add(
            appkey,
            name="总经理",
            parent_id=0,
            organization_id=organization_id,
            rule_group_id=rule_group_id,
            description="总经理",
            remark="总经理remark",
        )
        position_id_2 = self.position_add(
            appkey,
            name="研发总监",
            parent_id=position_id,
            organization_id=organization_id_2,
            rule_group_id=rule_group_id,
            description="研发总监",
            remark="研发总监",
        )
        position_id_3 = self.position_add(
            appkey,
            name="项目经理",
            parent_id=position_id_2,
            organization_id=organization_id_2,
            rule_group_id=rule_group_id,
            description="项目经理",
            remark="项目经理",
        )
        self.position_update(
            position_id_3,
            name='大项目经理',
            remark="大项目经理备注",
            organization_id=organization_id,
            rule_group_id=rule_group_id,
            description="大项目经理描述"
        )
        self.position_all(appkey)
        self.position_remove(position_id_2)

        # 6、 绑定客户
        self.bind_position(
            appkey,
            organization_id=organization_id_2,
            position_id=position_id,
            person_id=self.staff.id,
        )

        # 7、 获取客户权限
        self.get_permission(
            appkey,
            self.staff.id,
        )
