# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-09-02 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_tool', '0005_auto_20200826_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsrecord',
            name='source_type',
            field=models.CharField(choices=[('crm', 'crm'), ('customer', '客户端'), ('customer_wechat', '客户端微信小程序')], max_length=64, verbose_name='接收短信的用户来源平台'),
        ),
    ]