# Generated by Django 2.1.1 on 2018-12-28 03:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20181217_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expired_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 27, 11, 19, 23, 300532)),
        ),
    ]