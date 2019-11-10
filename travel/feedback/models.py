from django.db import models
from django.conf import settings
from mixins.models import TimestampMixin
# Create your models here.


class Feedback(TimestampMixin):
    class Meta:
        verbose_name = 'Запрос клиента'
        verbose_name_plural = 'Запросы клиента'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feedbacks', on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return '{}'.format(self.user)
