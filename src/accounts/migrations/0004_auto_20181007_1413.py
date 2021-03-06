# Generated by Django 2.0 on 2018-10-07 14:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_confirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmation',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 8, 14, 13, 50, 944596, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='confirmation',
            name='visited',
            field=models.BooleanField(default=False),
        ),
    ]
