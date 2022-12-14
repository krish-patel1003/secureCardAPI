# Generated by Django 4.1.3 on 2022-11-27 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0003_token'),
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='token',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='card.token'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='TransactionDetails',
        ),
    ]
