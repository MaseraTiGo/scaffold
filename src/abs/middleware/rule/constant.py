# coding=UTF-8

from abs.middleware.rule.base import BaseRule
from abs.middleware.rule.entity import RuleEntity


class Action(object):
    QUERY = ("query", "查询")
    MODELQUERY = ("modelquery", "型号查询")
    ADD = ("add", "添加")
    MODELADD = ("modeladd", "型号添加")
    EDIT = ("edit", "编辑")
    MODELEDIT = ("modeledit", "型号编辑")
    DELETE = ("delete", "删除")
    MODELDELETE = ("modeldelete", "删除型号")
    SETSTATUS = ("setstatus", "设置状态")
    SETONLINE = ("setonline", "设置上下线")
    LOOK = ("look", "查看")
    CLOSE = ("close", "关闭")
    REFRESH = ("refresh", "刷新")
    MSGPUSH = ("msgpush", "消息推送")
    INITIAL = ("initial", "初始化")

class Permise(BaseRule):
    DEFAULT = RuleEntity("permise", "权限管理")

    DEFAULT_DEPARTMENT = RuleEntity("department", "部门管理")
    DEFAULT_DEPARTMENT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_DEPARTMENT_ADD = RuleEntity(*Action.ADD)
    DEFAULT_DEPARTMENT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_DEPARTMENT_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_ROLE = RuleEntity("role", "角色管理")
    DEFAULT_ROLE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ROLE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_ROLE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_ROLE_DEL = RuleEntity(*Action.DELETE)


class Staff(BaseRule):
    DEFAULT = RuleEntity("staff", "员工管理")

    DEFAULT_ROSTER = RuleEntity("roster", "花名册")
    DEFAULT_ROSTER_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ROSTER_ADD = RuleEntity(*Action.ADD)
    DEFAULT_ROSTER_EDIT = RuleEntity(*Action.EDIT)

    DEFAULT_STAFF = RuleEntity("staff", "员工列表")
    DEFAULT_STAFF_QUERY = RuleEntity(*Action.QUERY)


class Product(BaseRule):
    DEFAULT = RuleEntity("product", "产品管理")

    DEFAULT_PRODUCT = RuleEntity("product", "产品列表")
    DEFAULT_PRODUCT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_PRODUCT_ADD = RuleEntity(*Action.ADD)
    DEFAULT_PRODUCT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_PRODUCT_DEL = RuleEntity(*Action.DELETE)

    # DEFAULT_PRODUCTMODEL = RuleEntity("productmodel", "型号管理")
    DEFAULT_PRODUCT_MODELQUERY = RuleEntity(*Action.MODELQUERY)
    DEFAULT_PRODUCT_MODELADD = RuleEntity(*Action.MODELADD)
    DEFAULT_PRODUCT_MODELEDIT = RuleEntity(*Action.MODELEDIT)
    DEFAULT_PRODUCT_MODELDEL = RuleEntity(*Action.MODELDELETE)


class Communication(BaseRule):
    DEFAULT = RuleEntity("communication", "客服管理")

    DEFAULT_COMMUNICATION = RuleEntity("communication", "产品列表")
    DEFAULT_COMMUNICATION_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_COMMUNICATION_ADD = RuleEntity(*Action.ADD)
    DEFAULT_COMMUNICATION_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_COMMUNICATION_DEL = RuleEntity(*Action.DELETE)
    DEFAULT_COMMUNICATION_SETONLINE = RuleEntity(*Action.SETONLINE)
    DEFAULT_COMMUNICATION_SETSTATUS = RuleEntity(*Action.SETSTATUS)

    DEFAULT_CHAT = RuleEntity("chat", "工作台")
    DEFAULT_CHAT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_CHAT_CLOSE = RuleEntity(*Action.CLOSE)
    DEFAULT_CHAT_SETONLINE = RuleEntity(*Action.SETONLINE)

    DEFAULT_FAQ = RuleEntity("faq", "工作台")
    DEFAULT_FAQ_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_FAQ_ADD = RuleEntity(*Action.ADD)
    DEFAULT_FAQ_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_FAQ_DEL = RuleEntity(*Action.DELETE)

class Eventonlineservice(BaseRule):
    DEFAULT = RuleEntity("eventonlineservice", "工单管理")

    DEFAULT_EVENTONLINESERVICE = RuleEntity("eventonlineservice", "工单列表")
    DEFAULT_EVENTONLINESERVICE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_EVENTONLINESERVICE_SETSTATUS = RuleEntity(*Action.SETSTATUS)
    DEFAULT_EVENTONLINESERVICE_DEL = RuleEntity(*Action.DELETE)
    DEFAULT_EVENTONLINESERVICE_LOOK = RuleEntity(*Action.LOOK)
    DEFAULT_EVENTONLINESERVICE_REFRESH = RuleEntity(*Action.REFRESH)

class WechatManage(BaseRule):
    DEFAULT = RuleEntity("wechatmanage", "公众号管理")

    DEFAULT_ADDOPERATE = RuleEntity("addoperate", "公众号添加")
    DEFAULT_ADDOPERATE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ADDOPERATE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_ADDOPERATE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_ADDOPERATE_DEL = RuleEntity(*Action.DELETE)
    DEFAULT_ADDOPERATE_INIT = RuleEntity(*Action.INITIAL)

    DEFAULT_ACCOUNTMANAGE = RuleEntity("accountmanage", "公众号管理")
    DEFAULT_ACCOUNTMANAGE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ACCOUNTMANAGE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_ACCOUNTMANAGE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_ACCOUNTMANAGE_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_PUSHHISTORY = RuleEntity("pushhistory", "推送历史")
    DEFAULT_PUSHHISTORY_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_PUSHHISTORY_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_FUNSMANAGE = RuleEntity("funsmanage", "粉丝管理")
    DEFAULT_FUNSMANAGE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_FUNSMANAGE_REFRESH = RuleEntity(*Action.REFRESH)
    DEFAULT_FUNSMANAGE_MSGPUSH = RuleEntity(*Action.MSGPUSH)

    DEFAULT_STORE = RuleEntity("store", "素材库")
    DEFAULT_STORE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_STORE_DEL = RuleEntity(*Action.DELETE)
    DEFAULT_STORE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_STORE_EDIT = RuleEntity(*Action.EDIT)

permise_rules = Permise()
staff_rules = Staff()
product_rules = Product()
communication_rules = Communication()
eventonlineservice_rules = Eventonlineservice()
wechatmanage_rules = WechatManage()
