# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-26 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_tool', '0004_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsrecord',
            name='scene',
            field=models.CharField(choices=[('register', '注册验证码'), ('forget', '找回密码验证码'), ('bindcard', '绑定银行卡'), ('login', '登陆'), ('wechat_register', '微信注册验证码')], max_length=64, verbose_name='场景标识'),
        ),
    ]
