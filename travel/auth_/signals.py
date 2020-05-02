from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import MainUser
import os
import logging

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=MainUser)
def tas_post_del(sender, instance, **kwargs):
    try:
        if instance.avatar:
             if os.path.isfile(instance.avatar.path):
                os.remove(instance.avatar.path)
    except Exception as e:
        logger.error(e)
