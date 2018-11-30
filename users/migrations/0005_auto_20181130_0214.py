# Generated by Django 2.1.1 on 2018-11-30 02:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181129_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='expired_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 30, 2, 14, 13, 320561)),
        ),
    ]
