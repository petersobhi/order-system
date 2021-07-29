# Generated by Django 3.2.5 on 2021-07-17 20:38

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='EUR', max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EGP', 'Egyptian Pound'), ('EUR', 'Euro'), ('USD', 'US Dollar')], default='EUR', editable=False, max_length=3),
        ),
    ]
