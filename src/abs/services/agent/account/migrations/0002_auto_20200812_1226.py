# Generated by Django 3.0.3 on 2020-08-12 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffaccount',
            name='head_url',
            field=models.CharField(default='', max_length=256, verbose_name='头像URL'),
        ),
        migrations.AddField(
            model_name='staffaccount',
            name='nick',
            field=models.CharField(default='', max_length=32, verbose_name='昵称'),
        ),
    ]
