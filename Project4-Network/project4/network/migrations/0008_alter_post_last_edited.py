# Generated by Django 4.1.4 on 2023-01-14 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_liking_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='last_edited',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
