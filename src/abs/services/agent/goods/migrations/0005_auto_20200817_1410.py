# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-17 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent_goods', '0004_auto_20200813_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='relations_id',
            field=models.IntegerField(default=0, verbose_name='学校专业id'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='years_id',
            field=models.IntegerField(default=0, verbose_name='学年id'),
        ),
    ]
