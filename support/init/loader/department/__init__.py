# coding=UTF-8

from support.init.base import BaseLoader


class DepartmentLoader(BaseLoader):

    def load(self):
        return [
            {
                'name': '公司',
                'parent': "",
                'describe': "公司",
            },
            {
                'name': '电商部',
                'parent': "公司",
                'describe': "电商部",
            },
            {
                'name': '电商售前一组',
                'parent': "电商部",
                'describe': "电商售前一组",
            },
            {
                'name': '电商售前二组',
                'parent': "电商部",
                'describe': "电商售前二组",
            },
            {
                'name': '增值部',
                'parent': "公司",
                'describe': "增值部",
            },
            {
                'name': '增值一部',
                'parent': "增值部",
                'describe': "增值一部",
            },
            {
                'name': '增值二部',
                'parent': "增值部",
                'describe': "增值二部",
            },
            {
                'name': '增值三部',
                'parent': "增值部",
                'describe': "增值三部",
            },
            {
                'name': '增值四部',
                'parent': "增值部",
                'describe': "增值四部",
            },
            {
                'name': '研发部',
                'parent': "公司",
                'describe': "研发部",
            },
            {
                'name': '招商业务部',
                'parent': "公司",
                'describe': "招商业务部",
            },
            {
                'name': '人事财务部',
                'parent': "公司",
                'describe': "人事财务部",
            },
            {
                'name': '微商售前部',
                'parent': "公司",
                'describe': "微商售前部",
            },
            {
                'name': '微商售后部',
                'parent': "公司",
                'describe': "微商售后部",
            },
            {
                'name': '微商售后组',
                'parent': "微商售后部",
                'describe': "微商售后组",
            },
            {
                'name': '电商售后组',
                'parent': "微商售后部",
                'describe': "电商售后组",
            },
            {
                'name': '新媒体客服部',
                'parent': "公司",
                'describe': "新媒体客服部",
            },
            {
                'name': '新媒体运营部',
                'parent': "公司",
                'describe': "新媒体运营部",
            },
            {
                'name': '电商运营部',
                'parent': "公司",
                'describe': "电商运营部",
            },
            {
                'name': '物流部',
                'parent': "公司",
                'describe': "物流部",
            },
            {
                'name': '后勤技术部',
                'parent': "公司",
                'describe': "后勤技术部",
            },
            {
                'name': '质检部',
                'parent': "公司",
                'describe': "质检部",
            },
            {
                'name': '微信运维部',
                'parent': "公司",
                'describe': "微信运维部",
            },
        ]
