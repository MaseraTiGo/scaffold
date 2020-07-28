# Generated by Django 3.0.3 on 2020-07-24 17:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('title', models.CharField(max_length=256, verbose_name='商品标题')),
                ('slideshow', models.TextField(verbose_name='商品轮播图')),
                ('video_display', models.TextField(verbose_name='展示视频')),
                ('detail', models.TextField(verbose_name='商品详情')),
                ('market_price', models.IntegerField(verbose_name='市场价格，单位：分')),
                ('pay_types', models.CharField(max_length=128, verbose_name='支付方式')),
                ('pay_services', models.CharField(max_length=128, verbose_name='支付服务')),
                ('despatch_type', models.CharField(choices=[('logistics', '物流交付'), ('offline', '线下交付'), ('online', '线上交付')], max_length=64, verbose_name='发货方式')),
                ('use_status', models.CharField(choices=[('enable', '启用'), ('forbiddent', '禁用')], default='forbiddent', max_length=64, verbose_name='使用状态')),
                ('company_id', models.IntegerField(verbose_name='公司ID')),
                ('production_id', models.IntegerField(verbose_name='产品ID')),
                ('remark', models.TextField(verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'moddleground_merchandise_base',
                'unique_together': {('company_id', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('show_image', models.IntegerField(verbose_name='展示图片')),
                ('sale_price', models.IntegerField(verbose_name='销售价格，单位：分')),
                ('stock', models.IntegerField(verbose_name='库存')),
                ('remark', models.TextField(verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('merchandise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchandise.Merchandise')),
            ],
            options={
                'db_table': 'moddleground_merchandise_specification',
            },
        ),
        migrations.CreateModel(
            name='SpecificationValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('category', models.CharField(max_length=24, verbose_name='属性分类')),
                ('attribute', models.CharField(max_length=64, verbose_name='属性值')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchandise.Specification')),
            ],
            options={
                'db_table': 'moddleground_merchandise_specification_value',
            },
        ),
    ]
