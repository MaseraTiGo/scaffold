# Generated by Django 3.0.3 on 2020-07-05 22:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerTransactionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑编码')),
                ('number', models.CharField(max_length=48, verbose_name='交易编号')),
                ('amount', models.IntegerField(verbose_name='金额，单位：分')),
                ('pay_type', models.CharField(choices=[('bank', '银行'), ('alipay', '支付宝'), ('wechat', '微信'), ('balance', '余额')], max_length=12, verbose_name='支付方式')),
                ('remark', models.TextField(default='', verbose_name='记录备注')),
                ('input_record_id', models.IntegerField(null=True, verbose_name='入账单ID')),
                ('output_record_id', models.IntegerField(null=True, verbose_name='出账单ID')),
                ('business_type', models.CharField(choices=[('order', '订单'), ('balance', '余额')], max_length=16, verbose_name='业务来源')),
                ('business_id', models.IntegerField(verbose_name='业务ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Customer')),
            ],
            options={
                'db_table': 'customer_transaction_record',
            },
        ),
        migrations.CreateModel(
            name='CustomerTransactionOutputRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑编码')),
                ('number', models.CharField(max_length=48, verbose_name='出账交易编号')),
                ('amount', models.IntegerField(verbose_name='金额，单位：分')),
                ('pay_type', models.CharField(choices=[('bank', '银行'), ('alipay', '支付宝'), ('wechat', '微信'), ('balance', '余额')], max_length=12, verbose_name='支付方式')),
                ('status', models.CharField(choices=[('pay_finish', '付款成功'), ('transaction_dealing', '交易处理中'), ('account_finish', '到账成功')], default='pay_finish', max_length=24, verbose_name='交易状态')),
                ('remark', models.TextField(default='', verbose_name='记录备注')),
                ('business_type', models.CharField(choices=[('order', '订单'), ('balance', '余额')], max_length=16, verbose_name='业务来源')),
                ('business_id', models.IntegerField(verbose_name='业务ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Customer')),
                ('transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.CustomerTransactionRecord')),
            ],
            options={
                'db_table': 'customer_transaction_output_record',
            },
        ),
        migrations.CreateModel(
            name='CustomerTransactionInputRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑编码')),
                ('number', models.CharField(max_length=48, verbose_name='入账交易编号')),
                ('amount', models.IntegerField(verbose_name='金额，单位：分')),
                ('pay_type', models.CharField(choices=[('bank', '银行'), ('alipay', '支付宝'), ('wechat', '微信'), ('balance', '余额')], max_length=12, verbose_name='支付方式')),
                ('status', models.CharField(choices=[('pay_finish', '付款成功'), ('transaction_dealing', '交易处理中'), ('account_finish', '到账成功')], default='pay_finish', max_length=24, verbose_name='交易状态')),
                ('remark', models.TextField(default='', verbose_name='记录备注')),
                ('business_type', models.CharField(choices=[('order', '订单'), ('balance', '余额')], max_length=16, verbose_name='业务来源')),
                ('business_id', models.IntegerField(verbose_name='业务ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Customer')),
                ('transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.CustomerTransactionRecord')),
            ],
            options={
                'db_table': 'customer_transaction_input_record',
            },
        ),
        migrations.CreateModel(
            name='CustomerBalanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=64, unique=True, verbose_name='唯一逻辑编码')),
                ('number', models.CharField(max_length=48, verbose_name='交易编号')),
                ('amount', models.IntegerField(verbose_name='金额，单位：分')),
                ('pay_type', models.CharField(choices=[('bank', '银行'), ('alipay', '支付宝'), ('wechat', '微信'), ('balance', '余额')], max_length=12, verbose_name='支付方式')),
                ('remark', models.TextField(default='', verbose_name='记录备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Customer')),
                ('input_record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.CustomerTransactionInputRecord')),
                ('output_record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.CustomerTransactionOutputRecord')),
            ],
            options={
                'db_table': 'customer_balance_record',
            },
        ),
    ]
