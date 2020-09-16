# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, \
        timezone, ForeignKey, CASCADE
from abs.services.agent.contract.settings import DB_PREFIX
from abs.services.agent.contract.utils.constant import TemplateStatus


class Template(BaseModel):
    agent_id = IntegerField(verbose_name = "代理商id", default = 0)
    name = CharField(verbose_name = "合同名称", max_length = 64, default = "")
    pdf_url = CharField(verbose_name = "合同模板pdf链接", max_length = 256, default = "")
    background_img_url = TextField(verbose_name = "合同背景图片", default = '[]')
    status = CharField(
        verbose_name = "状态",
        max_length = 32,
        choices = TemplateStatus.CHOICES,
        default = TemplateStatus.DRAFT
    )

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "template"

    @classmethod
    def search(cls, **attrs):
        template_qs = cls.query().filter(**attrs)
        return template_qs


class TemplateParam(BaseModel):
    template = ForeignKey(Template, on_delete = CASCADE)
    param_id = IntegerField(verbose_name = "参数id", default = 0)
    page_number = IntegerField(verbose_name = "页码", default = 0)
    coordinate_x = IntegerField(verbose_name = "参数位置x坐标", default = "0")
    coordinate_y = IntegerField(verbose_name = "参数位置y坐标", default = "0")
    width = IntegerField(verbose_name = "参数宽度", default = "0")
    height = IntegerField(verbose_name = "参数高度", default = "0")
    content = TextField(verbose_name = "参数冗余配置")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "template_param"

    @classmethod
    def search(cls, **attrs):
        template_param_qs = cls.query().filter(**attrs)
        return template_param_qs
