# Generated by Django 2.2.6 on 2019-11-03 11:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20191103_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f03406d9-259b-49cd-80f0-b8944a7f45ac'), unique=True, verbose_name='Номер билета'),
        ),
    ]
