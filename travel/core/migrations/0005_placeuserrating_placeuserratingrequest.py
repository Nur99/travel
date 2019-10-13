# Generated by Django 2.2.6 on 2019-10-13 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_auto_20191006_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceUserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('declined', 'declined')], default='pending', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_set', to='core.Place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Оценка пользователя залу',
                'verbose_name_plural': 'Оценки пользователей залам',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='PlaceUserRatingRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_set_2', to='core.Place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_set_2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Copy fitness user_rating',
                'verbose_name_plural': 'Copy fitness user_rating',
                'ordering': ['-timestamp'],
                'unique_together': {('place', 'user')},
            },
        ),
    ]
