# Generated by Django 3.0.3 on 2020-08-04 12:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('nick', models.CharField(max_length=32, verbose_name='昵称')),
                ('head_url', models.CharField(default='', max_length=256, verbose_name='头像URL')),
                ('work_number', models.CharField(max_length=24, verbose_name='工号')),
                ('is_admin', models.BooleanField(default=False, verbose_name='是否是管理员')),
                ('person_id', models.IntegerField(verbose_name='用户id')),
                ('company_id', models.IntegerField(verbose_name='企业id')),
                ('remark', models.TextField(verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'controller_staff_base',
            },
        ),
    ]