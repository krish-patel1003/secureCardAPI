# Generated by Django 4.1.3 on 2022-12-08 10:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0008_alter_card_consumer'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='issuerId',
            field=models.CharField(default='000', max_length=3, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
