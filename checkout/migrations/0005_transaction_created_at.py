# Generated by Django 4.1.3 on 2022-12-09 07:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_transaction_consumer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 12, 49, 7, 233300)),
        ),
    ]