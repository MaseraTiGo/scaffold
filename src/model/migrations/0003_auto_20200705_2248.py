# Generated by Django 3.0.3 on 2020-07-05 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0002_customerbalancerecord_customertransactioninputrecord_customertransactionoutputrecord_customertransac'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customertransactioninputrecord',
            name='business_id',
            field=models.IntegerField(null=True, verbose_name='业务ID'),
        ),
        migrations.AlterField(
            model_name='customertransactionoutputrecord',
            name='business_id',
            field=models.IntegerField(null=True, verbose_name='业务ID'),
        ),
        migrations.AlterField(
            model_name='customertransactionrecord',
            name='business_id',
            field=models.IntegerField(null=True, verbose_name='业务ID'),
        ),
    ]
