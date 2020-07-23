# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, CASCADE,\
        IntegerField, CharField, DateTimeField, TextField,\
        ForeignKey, timezone
from abs.middleground.business.production.settings import DB_PREFIX
from abs.middleground.business.production.store.entity.brand import \
        Brand


class Production(BaseModel):
    """
    产品信息

    attribute_list:[
        {
            category: "名称",
            attribute_list: [
                 "属性值",
                 "属性值",
                 "属性值",
                 .....
            ]
        }
        .....
    ]

    workflow_list:[
        {
            name: "名称",
            type: "事件",
            description: "描述",
        }
        .....
    ]
    """
    name = CharField(verbose_name="产品名称", max_length=24)
    description = CharField(verbose_name="品牌描述", max_length=256)

    attribute_list = TextField(verbose_name="属性json")
    workflow_list = TextField(verbose_name="流程json")

    brand = ForeignKey(Brand, on_delete=CASCADE)
    company_id = IntegerField(verbose_name="公司ID")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "production"
