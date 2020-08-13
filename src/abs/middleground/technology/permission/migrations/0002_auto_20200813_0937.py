# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-13 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='use_status',
            field=models.CharField(choices=[('enable', '启动'), ('forbidden', '禁用')], default='forbidden', max_length=24, verbose_name='使用状态'),
        ),
    ]
