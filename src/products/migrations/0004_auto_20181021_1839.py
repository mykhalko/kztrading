# Generated by Django 2.0 on 2018-10-21 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20181018_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(default='defvalue', max_length=128, unique=True),
            preserve_default=False,
        ),
    ]
