# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-09-22 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('name', models.CharField(max_length=32, verbose_name='公司名称')),
                ('license_number', models.CharField(max_length=32, verbose_name='营业执照编号')),
                ('permission_key', models.CharField(default='', max_length=256, verbose_name='权限appkey')),
                ('company_id', models.IntegerField(verbose_name='企业id')),
                ('remark', models.TextField(verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'crm_staff_company',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('work_number', models.CharField(max_length=24, verbose_name='工号')),
                ('is_admin', models.BooleanField(default=False, verbose_name='是否是管理员')),
                ('person_id', models.IntegerField(verbose_name='用户id')),
                ('permission_id', models.IntegerField(default=None, null=True, verbose_name='权限id')),
                ('remark', models.TextField(verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('name', models.CharField(default='', max_length=32, verbose_name='姓名')),
                ('phone', models.CharField(default='', max_length=20, verbose_name='手机号')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_staff.Company')),
            ],
            options={
                'db_table': 'crm_staff_base',
            },
        ),
    ]
