# Generated by Django 2.0 on 2018-10-08 16:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20181008_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmation',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 9, 16, 44, 58, 727593, tzinfo=utc)),
        ),
    ]
