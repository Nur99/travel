# Generated by Django 2.2.6 on 2019-12-02 21:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20191203_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('9e26687f-678d-4f3d-b875-0a343e92a00d'), unique=True, verbose_name='Номер билета'),
        ),
    ]
