# Generated by Django 3.1.1 on 2020-09-13 02:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auto_20200913_0227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='listing',
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('listing', models.ManyToManyField(blank=True, default=None, related_name='watchlist', to='auctions.Listing')),
                ('user', models.ManyToManyField(blank=True, default=None, related_name='user_watchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
