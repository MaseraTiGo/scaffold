# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, \
        timezone, DateField
from abs.services.agent.staff.settings import DB_PREFIX
from abs.middleground.business.person.utils.constant import EducationTypes


class Staff(BaseModel):

    nick = CharField(verbose_name = "昵称", max_length = 32)
    name = CharField(verbose_name = "姓名", max_length = 32, default = "")
    phone = CharField(verbose_name = "手机号", max_length = 20, default = "")
    head_url = CharField(verbose_name = "头像URL", max_length = 256, default = "")

    work_number = CharField(verbose_name = "工号", max_length = 24)
    is_admin = BooleanField(verbose_name = "是否是管理员", default = False)

    person_id = IntegerField(verbose_name = "用户id")
    company_id = IntegerField(verbose_name = "企业id")
    agent_id = IntegerField(verbose_name = "代理商id", default = 0)

    identification = CharField(verbose_name = "身份证号", max_length = 64, default = "")
    entry_time = DateField(verbose_name = "入职时间", null = True, blank = True)
    address = CharField(verbose_name = "家庭住址", max_length = 256, default = "")
    emergency_contact = CharField(verbose_name = "紧急联系人", max_length = 64, default = "")
    emergency_phone = CharField(verbose_name = "紧急联系人电话", max_length = 20, default = "")
    education = CharField(verbose_name = "学历", max_length = 24, choices = EducationTypes.CHOICES, \
                          default = EducationTypes.OTHER)
    bank_number = CharField(verbose_name = "银行卡号", max_length = 32, default = "")
    contract = CharField(verbose_name = "合同编号", max_length = 128, default = "")
    diploma_img = TextField(verbose_name = "毕业证书", default = '[]')

    remark = TextField(verbose_name = "备注")
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        staff_qs = cls.query().filter(**attrs)
        return staff_qs
