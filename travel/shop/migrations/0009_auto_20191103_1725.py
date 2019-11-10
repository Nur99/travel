# Generated by Django 2.2.6 on 2019-11-03 11:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20191103_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('06044176-69ce-4c2d-8c34-259672336aef'), unique=True, verbose_name='Номер билета'),
        ),
    ]