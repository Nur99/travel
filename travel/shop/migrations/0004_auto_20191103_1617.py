# Generated by Django 2.2.6 on 2019-11-03 10:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20191103_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='shop.Order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('4b90162a-6fe4-4926-bc0f-2f316764e60a'), unique=True, verbose_name='Номер билета'),
        ),
    ]
