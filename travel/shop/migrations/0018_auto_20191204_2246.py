# Generated by Django 2.2.6 on 2019-12-04 16:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20191203_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('bb4e2ae1-a39a-4175-bec6-1ba5adab8a52'), unique=True, verbose_name='Номер билета'),
        ),
    ]
