# coding=UTF-8


import json
from support.common.maker import BaseLoader


class RoleLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '超级管理员',
                'parent': "",
                'describe': "超级角色",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '老板',
                'parent': "超级管理员",
                'describe': "老板",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '电商部售前主管',
                'parent': "老板",
                'describe': "电商部售前主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '电商售前组长',
                'parent': "电商部售前主管",
                'describe': "电商售前组长",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '电商售前组员',
                'parent': "电商售前组长",
                'describe': "电商售前组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值部主管',
                'parent': "老板",
                'describe': "增值部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值一部主管',
                'parent': "增值部主管",
                'describe': "增值一部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值一部组长',
                'parent': "增值一部主管",
                'describe': "增值一部组长",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值一部组员',
                'parent': "增值一部组长",
                'describe': "增值一部组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '数据录入员',
                'parent': "增值一部组长",
                'describe': "数据录入员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值二部主管',
                'parent': "增值部主管",
                'describe': "增值二部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值二部组员',
                'parent': "增值二部主管",
                'describe': "增值二部组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值三部主管',
                'parent': "增值部主管",
                'describe': "增值三部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值三部组员',
                'parent': "增值三部主管",
                'describe': "增值三部组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值四部主管',
                'parent': "增值部主管",
                'describe': "增值四部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '增值四部组员',
                'parent': "增值四部主管",
                'describe': "增值四部组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '新媒体客服部主管',
                'parent': "老板",
                'describe': "新媒体客服部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '新媒体组长',
                'parent': "新媒体客服部主管",
                'describe': "新媒体组长",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '新媒体组员',
                'parent': "新媒体组长",
                'describe': "新媒体组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '新媒体运营部主管',
                'parent': "老板",
                'describe': "新媒体运营部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '美工',
                'parent': "新媒体运营部主管",
                'describe': "美工",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '视频剪辑',
                'parent': "新媒体运营部主管",
                'describe': "视频剪辑",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '运营',
                'parent': "新媒体运营部主管",
                'describe': "运营",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '文案',
                'parent': "新媒体运营部主管",
                'describe': "文案",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '数据',
                'parent': "新媒体运营部主管",
                'describe': "数据",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': 'SEO',
                'parent': "新媒体运营部主管",
                'describe': "SEO",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '仓库主管',
                'parent': "老板",
                'describe': "仓库主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '仓管员',
                'parent': "仓库主管",
                'describe': "仓管员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '电商运营主管',
                'parent': "老板",
                'describe': "电商运营主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '电商运营组员',
                'parent': "电商运营主管",
                'describe': "电商运营组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '招商业务部主管',
                'parent': "老板",
                'describe': "招商业务部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '商务助理',
                'parent': "招商业务部主管",
                'describe': "商务助理",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '后勤技术部主管',
                'parent': "老板",
                'describe': "后勤技术部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '运维员',
                'parent': "后勤技术部主管",
                'describe': "运维员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '财务主管',
                'parent': "老板",
                'describe': "财务主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '财务员',
                'parent': "财务主管",
                'describe': "财务员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '财务主管',
                'parent': "老板",
                'describe': "财务主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '财务员',
                'parent': "财务主管",
                'describe': "财务员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '行政经理',
                'parent': "老板",
                'describe': "行政经理",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '行政员',
                'parent': "行政经理",
                'describe': "行政员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '人事主管',
                'parent': "老板",
                'describe': "人事主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '人事助理',
                'parent': "人事主管",
                'describe': "人事助理",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '人事专员',
                'parent': "人事主管",
                'describe': "人事专员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '培训主管',
                'parent': "老板",
                'describe': "培训主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '培训讲师',
                'parent': "培训主管",
                'describe': "培训讲师",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '质检部主管',
                'parent': "老板",
                'describe': "质检部主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '质检专员',
                'parent': "质检部主管",
                'describe': "质检专员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '微商售前主管',
                'parent': "老板",
                'describe': "微商售前主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '微商售前组长',
                'parent': "微商售前主管",
                'describe': "微商售前组长",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '微商售前组员',
                'parent': "微商售前组长",
                'describe': "微商售前组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '微商售后主管',
                'parent': "老板",
                'describe': "微商售后主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '微商售后组长',
                'parent': "微商售后主管",
                'describe': "微商售后组长",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '微商售后组员',
                'parent': "微商售后组长",
                'describe': "微商售后组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '电商售后组长',
                'parent': "微商售后主管",
                'describe': "电商售后组长",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '电商售后组员',
                'parent': "电商售后组长",
                'describe': "电商售后组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '微信运维主管',
                'parent': "老板",
                'describe': "微信运维主管",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '微信运维组员',
                'parent': "微信运维主管",
                'describe': "微信运维组员",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': '研发部项目经理',
                'parent': "老板",
                'describe': "研发部项目经理",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': 'WEB前端',
                'parent': "研发部项目经理",
                'describe': "WEB前端",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': 'UI设计师',
                'parent': "研发部项目经理",
                'describe': "UI设计师",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': 'Java开发工程师',
                'parent': "研发部项目经理",
                'describe': "Java开发工程师",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },
            {
                'name': 'Python开发工程师',
                'parent': "研发部项目经理",
                'describe': "Python开发工程师",
                'data_level': 'all',
                'data_security': False,
                'rules': json.dumps([])
            },

        ]
