# Generated by Django 2.1.1 on 2018-09-26 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_auto_20180926_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='device_type_id',
            field=models.IntegerField(choices=[('服务器', '服务器'), ('交换机', '交换机'), ('防火墙', '防火墙')], default=1, verbose_name='资产类型'),
        ),
    ]
