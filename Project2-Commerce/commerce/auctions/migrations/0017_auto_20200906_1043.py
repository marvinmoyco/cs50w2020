# Generated by Django 3.1.1 on 2020-09-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20200906_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='categories',
            field=models.TextField(blank=True, default='', null=True, unique=True),
        ),
    ]
