# Generated by Django 2.0 on 2019-01-01 09:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20190101_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expired_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 31, 17, 24, 31, 415834)),
        ),
    ]
