# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-09-18 16:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customer_personal', '0003_collectionrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('type', models.CharField(choices=[('function_error', '功能异常'), ('optimization_proposal', '优化建议'), ('complaint_proposal', '投诉建议'), ('other', '其它反馈')], default='other', max_length=128, verbose_name='意见反馈类型')),
                ('status', models.CharField(choices=[('wait_solve', '待解决'), ('resolved', '已解决'), ('closed', '已关闭')], default='wait_solve', max_length=128, verbose_name='状态')),
                ('img_url', models.TextField(default='[]', verbose_name='图片')),
                ('describe', models.TextField(verbose_name='描述')),
                ('remark', models.TextField(verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_personal.Customer')),
            ],
            options={
                'db_table': 'customer_personal_feedback',
            },
        ),
    ]