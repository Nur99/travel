from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from requests import Request
from mixins.models import TimestampMixin
from utils import constants, messages
from utils.paybox import get_sig
from utils.password import generate_password
import requests


class CallBack(TimestampMixin, models.Model):
    """
    Paybox callback logs
    """
    meta_text = models.TextField(blank=True)
    body_text = models.TextField(blank=True)
    get_text = models.TextField(blank=True)

    CHECK = 'CHECK'
    RESULT = 'RESULT'
    REFUND = 'REFUND'
    CAPTURE = 'CAPTURE'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'

    RESULTS = (
        (CHECK, CHECK),
        (RESULT, RESULT),
        (REFUND, REFUND),
        (CAPTURE, CAPTURE),
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE),
    )

    result = models.CharField(max_length=10, choices=RESULTS, default=RESULT)

    def __str__(self):
        return self.result


class PaymentManager(models.Manager):
    def from_order(self, order):
        payment = Payment.objects.create(order=order,
                                         user=order.user,
                                         description=order.get_payment_description(),
                                         price=order.event.price,
                                         quantity=order.quantity,
                                         total_price=order.total_price,
                                         status=constants.CREATED,
                                         email=order.user.email)
        return payment


class Payment(TimestampMixin, models.Model):
    """
    Paybox payments transaction model
    pg_order_id: id of PGPayment
    https://api.paybox.money/payment.php?pg_merchant_id=504178&pg_amount=2121&pg_currency=KZT&pg_description=2121&pg_testing_mode=1&pg_salt=j7aBIZrlGrbLroEo&pg_sig=5d12203cbf4eccecb35045ca0e9a074f
    v = {
        'pg_order_id': '1',
        'pg_merchant_id': '504178',
        'pg_amount': '2121',
        'pg_currency': 'KZT',
        'pg_description': '2121',
        'pg_salt': 'j7aBIZrlGrbLroEo',
        'pg_testing_mode': '1'
    }
    b'pg_payment_id=10058008&pg_amount=2121.00&pg_currency=KZT&pg_net_amount=2067.97&pg_ps_amount=2121&pg_ps_full_amount=2121&pg_ps_currency=KZT&pg_payment_system=EPAYWEBKZT&pg_description=2121&pg_result=1&pg_payment_date=2018-05-23+17%3A33%3A19&pg_can_reject=1&pg_user_phone=77778889922&pg_need_phone_notification=0&pg_user_contact_email=test%40mail.ru&pg_need_email_notification=1&pg_testing_mode=1&pg_captured=0&pg_card_pan=4405-64XX-XXXX-6150&pg_card_exp=09%2F25&pg_card_owner=TEST+TEST&pg_card_brand=VI&pg_salt=LjKOo9dWqnA9gDSn&pg_sig=0c1e6e1373ef161b6f17d81836be4469'
    """
    class Meta:
        ordering = ['-id']
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
    user = models.ForeignKey(settings.MAIN_USER_MODEL, on_delete=models.CASCADE,
                             related_name='payments')
    email = models.EmailField(max_length=200, blank=True, null=True)
    total_price = models.PositiveIntegerField(null=True)
    price = models.PositiveIntegerField(null=True)
    quantity = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=200)
    salt = models.CharField(max_length=100)
    card_pan = models.CharField(max_length=100, null=True, blank=True)
    refund_callback = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=constants.PAYMENT_STATUSES,
                              default=constants.CREATED, db_index=True)

    order = models.ForeignKey(settings.ORDER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    pg_payment_id = models.CharField(max_length=100, null=True, blank=True)
    pg_testing_mode = models.SmallIntegerField(default=1)

    objects = PaymentManager()

    def __str__(self):
        return '{} - {}'.format(self.description, self.total_price)

    def clean(self):
        if not self.reservation:
            raise ValidationError(message=messages.RESERVATION_REQUIRED)
        super(Payment, self).clean()

    def save(self, *args, **kwargs):
        if not self.salt:
            self.salt = self.get_salt()
        super(Payment, self).save(*args, **kwargs)

    def get_paybox_url(self, total_price=None):
        params = {
            'pg_order_id': self.id,
            'pg_merchant_id': settings.PB_MERCHANT_ID,
            'pg_amount': self.get_total_price(total_price),
            'pg_currency': 'KZT',
            'pg_description': self.description,
            'pg_salt': self.salt,
            'pg_testing_mode': settings.PB_TESTING,
            'pg_result_url': "http://127.0.0.1:8000/payment/paybox/result/",
            "pg_success_url": "http://127.0.0.1:8000/payment/paybox/success/",
            'pg_check_url': "http://127.0.0.1:8000/payment/paybox/check/",
            'pg_request_method': "POST",
            'pg_success_url_method': "POST",
            'pg_refund_url': "http://127.0.0.1:8000/payment/paybox/refund/",
            'pg_capture_url': "http://127.0.0.1:8000/payment/paybox/capture/",
            "pg_failure_url": "http://127.0.0.1:8000/payment/paybox/failure/",
            'pg_failure_url_method': 'POST'
        }
        if self.email or self.user.email:
            params['pg_user_contact_email'] = self.email or self.user.email
        # if self.user.phone:
        #     params['pg_user_phone'] = self.user.phone
        sig = get_sig(params)
        params['pg_sig'] = sig
        p = Request('GET', settings.PB_URL, params=params).prepare()
        return p.url

    @property
    def mock_url(self):
        return 'Nurymjan krasavchik'

    @staticmethod
    def get_salt():
        return generate_password(length=10)

    def success(self, body):
        self.order.success()
        self.status = constants.SUCCESS
        self.pg_payment_id = body.get('pg_payment_id')
        self.card_pan = body.get('pg_card_pan')
        self.save()

    def fail(self, body):
        self.order.fail()
        self.status = constants.FAILURE
        self.pg_payment_id = body.get('pg_payment_id')
        self.card_pan = body.get('pg_card_pan')
        self.save()
