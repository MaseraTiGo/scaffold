# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-09-24 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customer_personal', '0004_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('content', models.CharField(max_length=64, verbose_name='内容')),
                ('status', models.CharField(choices=[('read', '已读'), ('unread', '未读')], max_length=32, verbose_name='消息状态')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_messages', to='customer_personal.Customer')),
            ],
            options={
                'db_table': 'customer_personal_message',
            },
        ),
    ]
