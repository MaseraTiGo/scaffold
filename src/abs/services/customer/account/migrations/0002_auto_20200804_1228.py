# Generated by Django 3.0.3 on 2020-08-04 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraccount',
            name='role_type',
            field=models.CharField(choices=[('crm', '客户管理系统'), ('customer', '客户端'), ('controller', '中台管控端')], max_length=24, verbose_name='角色'),
        ),
    ]
