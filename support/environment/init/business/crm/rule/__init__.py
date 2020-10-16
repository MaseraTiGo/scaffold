# coding=UTF-8


from support.common.maker import BaseLoader


class RuleLoader(BaseLoader):

    def generate(self):
        return [
            {
                "name": "所有权限",
                "parent": "",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "所有权限",
                "remark": "",
                "code": "HyFV"
            },
            {
                "name": "组织结构",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "组织结构",
                "remark": "",
                "code": "Dong"
            },
            {
                "name": "权限组管理",
                "parent": "组织结构",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "权限组管理",
                "remark": "",
                "code": "JunA"
            },
            {
                "name": "查询",
                "parent": "权限组管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "dOnG"
            },
            {
                "name": "编辑",
                "parent": "权限组管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "AjUn"
            },
            {
                "name": "添加",
                "parent": "权限组管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "GJuN"
            },
            {
                "name": "删除",
                "parent": "权限组管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "AiYo"
            },
            {
                "name": "职位管理",
                "parent": "组织结构",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "职位管理",
                "remark": "",
                "code": "YoiA"
            },
            {
                "name": "查询",
                "parent": "职位管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "RpsV"
            },
            {
                "name": "编辑",
                "parent": "职位管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "UWQT"
            },
            {
                "name": "添加",
                "parent": "职位管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "CsUW"
            },
            {
                "name": "删除",
                "parent": "职位管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "FKJq"
            },
            {
                "name": "部门管理",
                "parent": "组织结构",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "部门管理",
                "remark": "",
                "code": "sbHL"
            },
            {
                "name": "查询",
                "parent": "部门管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "HXDP"
            },
            {
                "name": "编辑",
                "parent": "部门管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "Mnqf"
            },
            {
                "name": "添加",
                "parent": "部门管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "Rahh"
            },
            {
                "name": "删除",
                "parent": "部门管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "FsdC"
            },
            {
                "name": "员工列表",
                "parent": "组织结构",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "员工列表",
                "remark": "",
                "code": "vESs"
            },
            {
                "name": "查询",
                "parent": "员工列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "yFsB"
            },
            {
                "name": "编辑",
                "parent": "员工列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "aNcN"
            },
            {
                "name": "添加",
                "parent": "员工列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "Ypxy"
            },

            {
                "name": "编辑账号",
                "parent": "员工列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑账号",
                "remark": "",
                "code": "aNCN"
            },

            {
                "name": "编辑部门",
                "parent": "员工列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑部门",
                "remark": "",
                "code": "ANcN"
            },

            {
                "name": "客户管理",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "客户管理",
                "remark": "",
                "code": "rVxD"
            },
            {
                "name": "客户列表",
                "parent": "客户管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "客户列表",
                "remark": "",
                "code": "ANAc"
            },
            {
                "name": "查询",
                "parent": "客户列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "MGLV"
            },
            {
                "name": "详情",
                "parent": "客户列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "详情",
                "remark": "",
                "code": "MGLv"
            },
            {
                "name": "产品管理",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "产品管理",
                "remark": "",
                "code": "mUUq"
            },
            {
                "name": "品牌列表",
                "parent": "产品管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "品牌列表",
                "remark": "",
                "code": "xMhJ"
            },
            {
                "name": "查询",
                "parent": "品牌列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "dtuC"
            },
            {
                "name": "编辑",
                "parent": "品牌列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "YbRk"
            },
            {
                "name": "添加",
                "parent": "品牌列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "hohf"
            },
            {
                "name": "删除",
                "parent": "品牌列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "OVRK"
            },
            {
                "name": "产品列表",
                "parent": "产品管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "产品列表",
                "remark": "",
                "code": "wmce"
            },
            {
                "name": "查询",
                "parent": "产品列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "stli"
            },
            {
                "name": "编辑",
                "parent": "产品列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "HClb"
            },
            {
                "name": "添加",
                "parent": "产品列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "kkFG"
            },
            {
                "name": "删除",
                "parent": "产品列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "xoEv"
            },
            {
                "name": "商品管理",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "商品管理",
                "remark": "",
                "code": "KPtC"
            },
            {
                "name": "商品列表",
                "parent": "商品管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "商品列表",
                "remark": "",
                "code": "PxRg"
            },
            {
                "name": "查询",
                "parent": "商品列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "EJnV"
            },
            {
                "name": "上下架",
                "parent": "商品列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "上下架",
                "remark": "",
                "code": "EJvN"
            },
            {
                "name": "详情",
                "parent": "商品列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "详情",
                "remark": "",
                "code": "EJNV"
            },
            {
                "name": "置顶",
                "parent": "商品列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "置顶",
                "remark": "",
                "code": "EJnv"
            },
            {
                "name": "商品审核",
                "parent": "商品管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "商品审核",
                "remark": "",
                "code": "FyPY"
            },
            {
                "name": "查询",
                "parent": "商品审核",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "UYeY"
            },
            {
                "name": "详情",
                "parent": "商品审核",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "详情",
                "remark": "",
                "code": "UYEY"
            },
            {
                "name": "学校列表",
                "parent": "商品管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "学校列表",
                "remark": "",
                "code": "QvUa"
            },
            {
                "name": "查询",
                "parent": "学校列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "oAAt"
            },
            {
                "name": "详情",
                "parent": "学校列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "详情",
                "remark": "",
                "code": "oAAT"
            },
            {
                "name": "编辑",
                "parent": "学校列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "PJUS"
            },
            {
                "name": "添加",
                "parent": "学校列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "LBsk"
            },
            {
                "name": "删除",
                "parent": "学校列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "EQTV"
            },
            {
                "name": "置顶",
                "parent": "学校列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "置顶",
                "remark": "",
                "code": "EQTv"
            },
            {
                "name": "专业列表",
                "parent": "商品管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "专业列表",
                "remark": "",
                "code": "dris"
            },
            {
                "name": "查询",
                "parent": "专业列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "Iyvr"
            },
            {
                "name": "编辑",
                "parent": "专业列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "Qwcg"
            },
            {
                "name": "添加",
                "parent": "专业列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "WCdh"
            },
            {
                "name": "删除",
                "parent": "专业列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "EQXw"
            },
            {
                "name": "置顶",
                "parent": "专业列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "置顶",
                "remark": "",
                "code": "EQXW"
            },
            {
                "name": "合同管理",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "合同管理",
                "remark": "",
                "code": "KLQw"
            },
            {
                "name": "合同参数管理",
                "parent": "合同管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "合同参数管理",
                "remark": "",
                "code": "llOo"
            },
            {
                "name": "查询",
                "parent": "合同参数管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "JLsd"
            },
            {
                "name": "编辑",
                "parent": "合同参数管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "meQR"
            },
            {
                "name": "添加",
                "parent": "合同参数管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "AUiu"
            },
            {
                "name": "删除",
                "parent": "合同参数管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "HJiY"
            },
            {
                "name": "合同模板",
                "parent": "合同管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "合同模板",
                "remark": "",
                "code": "YUDE"
            },
            {
                "name": "查询",
                "parent": "合同模板",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "tifa"
            },
            {
                "name": "预览",
                "parent": "合同模板",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "预览",
                "remark": "",
                "code": "tifA"
            },
            {
                "name": "审核",
                "parent": "合同模板",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "审核",
                "remark": "",
                "code": "tIfA"
            },
            {
                "name": "短信列表",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "短信列表",
                "remark": "",
                "code": "uOrK"
            },
            {
                "name": "短信列表子项",
                "parent": "短信列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "短信列表子项",
                "remark": "",
                "code": "QnGB"
            },
            {
                "name": "查询",
                "parent": "短信列表子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "snpk"
            },
            {
                "name": "订单管理",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "订单管理",
                "remark": "",
                "code": "fGVe"
            },
            {
                "name": "订单列表",
                "parent": "订单管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "订单列表",
                "remark": "",
                "code": "uPlM"
            },
            {
                "name": "查询",
                "parent": "订单列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "DRQs"
            },
            {
                "name": "详情",
                "parent": "订单列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "详情",
                "remark": "",
                "code": "DRQS"
            },
            {
                "name": "合同列表",
                "parent": "订单管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "合同列表",
                "remark": "",
                "code": "hwFG"
            },
            {
                "name": "查询",
                "parent": "合同列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "EmdV"
            },
            {
                "name": "代理商",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "代理商",
                "remark": "",
                "code": "kCle"
            },
            {
                "name": "代理商列表",
                "parent": "代理商",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "代理商列表",
                "remark": "",
                "code": "naai"
            },
            {
                "name": "查询",
                "parent": "代理商列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "DscD"
            },
            {
                "name": "详情",
                "parent": "代理商列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "详情",
                "remark": "",
                "code": "DsCD"
            },
            {
                "name": "编辑",
                "parent": "代理商列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "GbAh"
            },
            {
                "name": "添加",
                "parent": "代理商列表",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "gkpH"
            },
            {
                "name": "广告管理",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "广告管理",
                "remark": "",
                "code": "HASY"
            },
            {
                "name": "广告位管理",
                "parent": "广告管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "广告位管理",
                "remark": "",
                "code": "FIos"
            },
            {
                "name": "查询",
                "parent": "广告位管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "JQpq"
            },
            {
                "name": "编辑",
                "parent": "广告位管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "ORGX"
            },
            {
                "name": "添加",
                "parent": "广告位管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "rscG"
            },
            {
                "name": "状态",
                "parent": "广告位管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "状态",
                "remark": "",
                "code": "SRcG"
            },
            {
                "name": "广告管理子项",
                "parent": "广告管理",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "广告管理子项",
                "remark": "",
                "code": "ahYj"
            },
            {
                "name": "查询",
                "parent": "广告管理子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "xfbN"
            },
            {
                "name": "编辑",
                "parent": "广告管理子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "blbP"
            },
            {
                "name": "添加",
                "parent": "广告管理子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "lcEU"
            },
            {
                "name": "删除",
                "parent": "广告管理子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "KUlF"
            },
            {
                "name": "状态",
                "parent": "广告管理子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "状态",
                "remark": "",
                "code": "KIIF"
            },
            {
                "name": "公告消息",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "公告消息",
                "remark": "",
                "code": "SAGI"
            },
            {
                "name": "公告消息子项",
                "parent": "公告消息",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "公告消息子项",
                "remark": "",
                "code": "NJSS"
            },
            {
                "name": "查询",
                "parent": "公告消息子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "ehHH"
            },
            {
                "name": "编辑",
                "parent": "公告消息子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "LydD"
            },
            {
                "name": "添加",
                "parent": "公告消息子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "添加",
                "remark": "",
                "code": "nGyR"
            },
            {
                "name": "删除",
                "parent": "公告消息子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "删除",
                "remark": "",
                "code": "BXVC"
            },
            {
                "name": "状态",
                "parent": "公告消息子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "状态",
                "remark": "",
                "code": "bxvc"
            },
            {
                "name": "意见反馈",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "公告消息",
                "remark": "",
                "code": "IVdU"
            },
            {
                "name": "意见反馈子项",
                "parent": "意见反馈",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "意见反馈子项",
                "remark": "",
                "code": "hMHH"
            },
            {
                "name": "查询",
                "parent": "意见反馈子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "TQcR"
            },
            {
                "name": "立即处理",
                "parent": "意见反馈子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "立即处理",
                "remark": "",
                "code": "Mroo"
            },
            {
                "name": "查询结果",
                "parent": "意见反馈子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询结果",
                "remark": "",
                "code": "MroO"
            },
            {
                "name": "系统设置",
                "parent": "所有权限",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "系统设置",
                "remark": "",
                "code": "weYR"
            },
            {
                "name": "系统设置子项",
                "parent": "系统设置",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "系统设置子项",
                "remark": "",
                "code": "BCxs"
            },
            {
                "name": "查询",
                "parent": "系统设置子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "查询",
                "remark": "",
                "code": "tfry"
            },
            {
                "name": "编辑",
                "parent": "系统设置子项",
                "platform_name": "橙鹿教育CRM总控平台",
                "description": "编辑",
                "remark": "",
                "code": "YubN"
            }
        ]
