from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from requests import Request
from mixins.models import TimestampMixin
from utils import constants, messages
import requests


class PaymentManager(models.Manager):
    def from_order(self, order):
        payment = Payment.objects.create(order=order,
                                         user=order.user,
                                         description=order.get_payment_description(),
                                         total_price=order.total_price,
                                         status=constants.CREATED,
                                        )
        return payment


class Payment(TimestampMixin, models.Model):
    class Meta:
        ordering = ['-id']
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='payments')
    card = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.PositiveIntegerField(null=True)
    description = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=10, choices=constants.PAYMENT_STATUSES,
                              default=constants.CREATED, db_index=True)
    order = models.ForeignKey(settings.ORDER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    objects = PaymentManager()

    def __str__(self):
        return '{} - {}'.format(self.description, self.total_price)

    def get_payment_url(self):
        p = Request('GET', settings.PAYMENT_URL.format(self.id)).prepare()
        return p.url

    def success(self, body):
        self.order.success()
        self.status = constants.SUCCESS
        self.save()

    def fail(self, body):
        self.order.fail()
        self.status = constants.FAILURE
        self.save()
