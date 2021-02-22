# Generated by Django 2.2.6 on 2019-12-06 15:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20191110_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8904fd31-c3c8-491c-b506-72824e248c41'), unique=True, verbose_name='Номер билета'),
        ),
    ]