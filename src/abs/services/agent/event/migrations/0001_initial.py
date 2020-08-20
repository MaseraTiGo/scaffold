# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-20 10:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrackEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('agent_staff_id', models.IntegerField(verbose_name='代理商员工id')),
                ('organization_id', models.IntegerField(verbose_name='组织id')),
                ('remark', models.TextField(default='', null=True, verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('person_id', models.IntegerField(default=0, verbose_name='用户id')),
                ('agent_id', models.IntegerField(verbose_name='代理商id')),
                ('agent_customer_id', models.IntegerField(default=0, verbose_name='代理商客户id')),
                ('describe', models.TextField(verbose_name='描述')),
                ('track_type', models.CharField(choices=[('phone', '电话'), ('wechat', '微信'), ('message', '短信'), ('email', '邮件'), ('other', '其它')], default='other', max_length=64, verbose_name='跟中类型')),
            ],
            options={
                'db_table': 'agent_event_base',
            },
        ),
    ]
