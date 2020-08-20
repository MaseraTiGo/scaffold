# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-20 17:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agent_goods', '0005_auto_20200817_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('phone', models.CharField(default='', max_length=16, verbose_name='手机号')),
                ('expire_date', models.DateField(verbose_name='过期天数')),
                ('remark', models.TextField(verbose_name='说明')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent_goods.Goods')),
            ],
            options={
                'db_table': 'agent_goods_poster',
            },
        ),
        migrations.CreateModel(
            name='PosterSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('specification_id', models.IntegerField(verbose_name='规格id')),
                ('sale_price', models.IntegerField(verbose_name='价格')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent_goods.Poster')),
            ],
            options={
                'db_table': 'agent_goods_poster_specification',
            },
        ),
    ]