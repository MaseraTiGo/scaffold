# Generated by Django 3.0.3 on 2020-08-12 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_staff', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='head_url',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='nick',
        ),
    ]