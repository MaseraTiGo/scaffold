# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-09-11 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent_goods', '0011_posterspecification_original_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='template_id',
            field=models.IntegerField(default=0, verbose_name='合同模板id'),
        ),
    ]