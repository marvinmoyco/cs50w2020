# Generated by Django 4.1.4 on 2023-01-14 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_liking_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liking',
            name='post',
            field=models.ManyToManyField(related_name='liked_post', to='network.post'),
        ),
    ]
