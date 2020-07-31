# Generated by Django 3.0.3 on 2020-07-30 20:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('despatch_type', models.CharField(choices=[('logistics', '物流交付'), ('phone_top_up', '手机充值'), ('eduction_contract', '教育合同')], max_length=64, verbose_name='发货方式')),
                ('despatch_id', models.IntegerField(verbose_name='发送ID')),
                ('remark', models.TextField(default='', verbose_name='记录备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'middleground_order_delivery_record',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('name', models.CharField(default='', max_length=16, verbose_name='姓名')),
                ('phone', models.CharField(default='', max_length=24, verbose_name='手机号')),
                ('address', models.CharField(default='', max_length=256, verbose_name='地址')),
                ('identification', models.CharField(default='', max_length=24, verbose_name='身份证号')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'middleground_order_invoice',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('actual_amount', models.IntegerField(verbose_name='实付金额，单位：分')),
                ('last_payment_type', models.CharField(choices=[('bank', '银行'), ('alipay', '支付宝'), ('wechat', '微信'), ('balance', '余额')], default=None, max_length=16, null=True, verbose_name='最后支付方式')),
                ('last_payment_time', models.DateTimeField(default=None, null=True, verbose_name='最后支付时间')),
                ('last_payment_amount', models.IntegerField(default=0, verbose_name='最后支付金额')),
                ('remark', models.TextField(default='', verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'middleground_order_payment',
            },
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('sale_price', models.IntegerField(verbose_name='销售价位，单位：分')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'middleground_order_requirement',
            },
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('amount', models.IntegerField(verbose_name='实付金额，单位：分')),
                ('pay_type', models.CharField(choices=[('bank', '银行'), ('alipay', '支付宝'), ('wechat', '微信'), ('balance', '余额')], default=None, max_length=16, null=True, verbose_name='支付方式')),
                ('output_record_id', models.IntegerField(null=True, verbose_name='出账凭证id')),
                ('remark', models.TextField(default='', verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Payment')),
            ],
            options={
                'db_table': 'middleground_order_payment_record',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('number', models.CharField(max_length=24, verbose_name='订单编号')),
                ('description', models.TextField(default='', verbose_name='订单描述')),
                ('remark', models.TextField(default='', verbose_name='备注')),
                ('strike_price', models.IntegerField(verbose_name='成交金额，单位：分')),
                ('status', models.CharField(choices=[('order_launched', '订单已下单'), ('payment_finished', '订单支已支付'), ('delivery_finished', '订单已发货'), ('order_closed', '订单关闭'), ('order_finished', '订单完成')], default='order_launched', max_length=24, verbose_name='订单状态')),
                ('launch_type', models.CharField(choices=[('company', '公司'), ('person', '个人')], max_length=16, verbose_name='发起方类型')),
                ('launch_id', models.IntegerField(verbose_name='发起方ID')),
                ('server_type', models.CharField(choices=[('company', '公司'), ('person', '个人')], max_length=16, verbose_name='服务方类型')),
                ('server_id', models.IntegerField(verbose_name='服务方ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Invoice')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Payment')),
                ('requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Requirement')),
            ],
            options={
                'db_table': 'middleground_order_order',
            },
        ),
        migrations.CreateModel(
            name='MerchandiseSnapShoot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('production_id', models.IntegerField(verbose_name='产品ID')),
                ('merchandise_id', models.IntegerField(verbose_name='商品ID')),
                ('specification_id', models.IntegerField(verbose_name='商品g规格ID')),
                ('title', models.CharField(max_length=256, verbose_name='商品标题')),
                ('show_image', models.CharField(max_length=256, verbose_name='展示图片')),
                ('remark', models.TextField(verbose_name='快照备注')),
                ('sale_price', models.IntegerField(verbose_name='销售单价，单位：分')),
                ('count', models.IntegerField(verbose_name='商品购买数量')),
                ('total_price', models.IntegerField(verbose_name='总价，单位：分')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Requirement')),
            ],
            options={
                'db_table': 'middleground_order_snapshoot',
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Requirement'),
        ),
        migrations.CreateModel(
            name='DeliveryRecordList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑码')),
                ('delivery_count', models.IntegerField(verbose_name='发货数量')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('delivery_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.DeliveryRecord')),
                ('snapshoot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.MerchandiseSnapShoot')),
            ],
            options={
                'db_table': 'middleground_order_delivery_record_list',
            },
        ),
        migrations.AddField(
            model_name='deliveryrecord',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Invoice'),
        ),
    ]
