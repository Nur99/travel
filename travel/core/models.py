# coding=utf-8
from django.contrib.auth import get_user_model
from django.db import models

from utils import constants

User = get_user_model()
# Create your models here.


class Country(models.Model):
    """
    Model for storing Cities from fitcom.kz
    """

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    name = models.CharField(max_length=100, verbose_name='Название страны',
                            unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Model for storing Cities from fitcom.kz
    """

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    name = models.CharField(max_length=100, verbose_name='Название города',
                            unique=True, null=False, blank=False)
    country = models.ForeignKey(Country, related_name='cities', on_delete=models.DO_NOTHING, verbose_name='Страна')

    def __str__(self):
        return self.name


class PlaceType(models.Model):
    """
    Model for storing types of places in fitcom.kz
    """

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    name = models.CharField(max_length=100, verbose_name='Название типа',
                            unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


class PlaceService(models.Model):
    """
    Model for storing service types of places in fitcom.kz
    """

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    name = models.CharField(max_length=100, verbose_name='Название услуги',
                            unique=True, null=False, blank=False)

    def __str__(self):
        return self.name
    

class Place(models.Model):
    """
    Model for storing places from fitcom.kz
    """

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'
        ordering = ('-rating', )

    name = models.CharField(max_length=10000, verbose_name='Название заведения',
                            null=False, blank=False)
    avatar_url = models.ImageField(upload_to='images/', blank=False, null=False, max_length=1000)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL,
                             related_name='places',
                             verbose_name='Город заведения')
    place_type = models.ForeignKey(PlaceType, null=True,
                                   on_delete=models.SET_NULL,
                                   related_name='places',
                                   verbose_name='Тип заведения')
    rating = models.FloatField(null=True, verbose_name='Рейтинг заведения',
                               default=0.0)
    review_count = models.IntegerField(default=0,
                                       verbose_name='Количество голосов')
    description = models.CharField(max_length=10000,
                                   verbose_name='Описание заведения', null=True,
                                   blank=True)
    address = models.CharField(max_length=10000, verbose_name='Адрес заведения',
                               null=True, blank=False)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    phones = models.CharField(max_length=10000, verbose_name='Телефоны заведения',
                              blank=True, null=True)
    website_url = models.CharField(max_length=10000,
                                   verbose_name='Ссылка на сайт',
                                   null=True, blank=True)
    working_hours = models.CharField(max_length=10000, verbose_name='Часы работы',
                                     null=True, blank=True)
    services = models.ManyToManyField(PlaceService, related_name='places',
                                      blank=True)
    price = models.PositiveIntegerField(verbose_name='Цена посещений', default=0)

    def recalculate_rating(self):
        from django.db.models import Avg
        ratings = self.rating_set_2
        value = 0
        if ratings.exists():
            value = ratings.aggregate(avg=Avg('rating'))['avg']
        self.rating_count = ratings.count()
        self.rating = value
        self.save()

    def __str__(self):
        return self.name


class PlaceUserRatingRequest(models.Model):
    class Meta:
        verbose_name = 'Copy fitness user_rating'
        verbose_name_plural = 'Copy fitness user_rating'
        ordering = ['-timestamp']
        unique_together = ('place', 'user')

    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='rating_set_2')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_set_2')
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}: {}'.format(self.place, self.user, self.rating)


class PlaceUserRatingManager(models.Manager):

    def add_rating(self, place, user, rating, review):
        # self.filter(user=user, fitness=fitness).update(latest=False)
        rating = PlaceUserRating(user=user, place=place, rating=rating, review=review)
        rating.save(admin_side=False)
        return rating

    def update_user_ratings(self, place, user):
        approved_user_ratings = PlaceUserRating.objects.filter(place=place, user=user, status=constants.FEEDBACK_APPROVED)
        copy, _ = PlaceUserRatingRequest.objects.get_or_create(place=place, user=user)

        if approved_user_ratings:
            last_approved_review = approved_user_ratings.first()
            copy.rating = last_approved_review.rating
            copy.review = last_approved_review.review
            copy.timestamp = last_approved_review.timestamp
            copy.save()
        else:
            copy.delete()
        place.recalculate_rating()


class PlaceUserRating(models.Model):
    class Meta:
        verbose_name = 'Оценка пользователя залу'
        verbose_name_plural = 'Оценки пользователей залам'
        ordering = ['-timestamp']

    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='rating_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_set')
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0)
    status = models.CharField(max_length=20,
                              choices=constants.FEEDBACK_STATUSES,
                              default=constants.FEEDBACK_PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PlaceUserRatingManager()

    def __str__(self):
        return '{} - {}: {}'.format(self.place, self.user, self.rating)

    def delete(self, admin_side=True, *args, **kwargs):
        super(PlaceUserRating, self).delete(*args, **kwargs)
        PlaceUserRating.objects.update_user_ratings(place=self.place, user=self.user)

    def save(self, admin_side=True, *args, **kwargs):
        super(PlaceUserRating, self).save(*args, **kwargs)
        PlaceUserRating.objects.update_user_ratings(place=self.place, user=self.user)

