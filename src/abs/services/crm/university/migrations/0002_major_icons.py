# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-06 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_university', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='major',
            name='icons',
            field=models.CharField(default='', max_length=256, verbose_name='专业图标'),
        ),
    ]
