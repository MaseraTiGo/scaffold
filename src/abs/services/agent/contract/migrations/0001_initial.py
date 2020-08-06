# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-06 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('customer_id', models.IntegerField(verbose_name='客户id')),
                ('agent_id', models.IntegerField(verbose_name='代理商id')),
                ('order_item_id', models.IntegerField(verbose_name='订单商品详情id')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('phone', models.CharField(default='', max_length=16, verbose_name='联系电话')),
                ('email', models.TextField(default='', max_length=32, verbose_name='emali')),
                ('identification', models.CharField(default='', max_length=24, verbose_name='身份证号')),
                ('autograph', models.CharField(default='', max_length=256, verbose_name='签名URL')),
                ('url', models.CharField(default='', max_length=256, verbose_name='合同url')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'agent_contract_base',
            },
        ),
    ]
