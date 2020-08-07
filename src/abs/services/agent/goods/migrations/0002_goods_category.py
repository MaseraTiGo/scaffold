# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-07 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent_goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='category',
            field=models.CharField(choices=[('undergraduate', '专升本'), ('specialty', '高起专'), ('graduate', '考研'), ('qualification', '资格证'), ('other', '其它')], default='other', max_length=64, verbose_name='类别'),
        ),
    ]