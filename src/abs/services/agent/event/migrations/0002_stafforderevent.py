<<<<<<< HEAD
# Generated by Django 3.0.3 on 2020-08-25 19:36
=======
# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-21 15:54
from __future__ import unicode_literals
>>>>>>> 4e14b84e61398abf05de06fad9c444cef3d552cc

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agent_event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffOrderEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('staff_id', models.IntegerField(default=0, verbose_name='员工id')),
                ('organization_id', models.IntegerField(verbose_name='组织id')),
                ('remark', models.TextField(default='', null=True, verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('order_id', models.IntegerField(verbose_name='订单id')),
            ],
            options={
                'db_table': 'agent_event_staff_order',
            },
        ),
    ]
