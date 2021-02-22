from django.conf import settings
from django.db import models
from mixins.models import TimestampMixin
from utils.upload import unique_path
from utils.constants import APPROVED, CANCELED, RESERVED, ORDER_STATUSES

# Create your models here.


import uuid


class Event(TimestampMixin):
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятий'

    title = models.CharField(max_length=200, verbose_name='Имя')
    place = models.ForeignKey(
        settings.PLACE_MODEL,
        related_name='events',
        on_delete=models.CASCADE,
        verbose_name='Место')
    image = models.ImageField(upload_to=unique_path, verbose_name='Фото')
    description = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0.0, verbose_name='Цена')
    note = models.TextField(verbose_name='Заметки (запреты, советы)')
    timestamp = models.DateTimeField(verbose_name='Время мероприятий')

    def __str__(self):
        return '{}'.format(self.title)


class Order(TimestampMixin):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
    event = models.ForeignKey(
        Event,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='Мероприятие')
    quantity = models.IntegerField(
        default=1,
        verbose_name='Количество')
    status = models.CharField(
        max_length=100,
        choices=ORDER_STATUSES,
        default=RESERVED,
        verbose_name='Статус заказа')

    @property
    def total_price(self):
        return self.quantity * self.event.price

    def get_payment_description(self):
        return '{}'.format(self.event)

    def success(self):
        self.status = APPROVED
        for i in range(self.quantity):
            Ticket.objects.create(order=self)
        self.save()

    def fail(self):
        self.status = CANCELED
        self.save()


class Ticket(models.Model):
    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

    order = models.ForeignKey(Order,
                              related_name='tickets',
                              on_delete=models.CASCADE,
                              verbose_name='Заказ')
    uuid = models.UUIDField(default=uuid.uuid4(),
                            unique=True,
                            verbose_name='Номер билета')


class Test(TimestampMixin):
    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

    title = models.CharField(max_length=200, verbose_name='Имя', null=True, default='Gi')
