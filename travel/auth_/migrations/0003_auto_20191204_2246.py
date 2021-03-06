# Generated by Django 2.2.6 on 2019-12-04 16:46

from django.db import migrations, models
import utils.file_utils


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0002_mainuser_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', validators=[utils.file_utils.validate_image_size]),
        ),
    ]
