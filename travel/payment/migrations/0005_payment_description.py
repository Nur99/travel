# Generated by Django 2.2.6 on 2019-11-10 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_payment_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
    ]