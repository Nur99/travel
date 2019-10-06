# coding=utf-8
from django.db import models

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

    def __str__(self):
        return self.name

