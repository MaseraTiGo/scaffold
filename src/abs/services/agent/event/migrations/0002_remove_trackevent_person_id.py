# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-08-20 12:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent_event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trackevent',
            name='person_id',
        ),
    ]