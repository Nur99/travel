import uuid
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from utils import constants, messages


class MainUserManager(BaseUserManager):
    """
       Main user manager
    """

    def create_user(self, email, password=None, first_name=None):
        """
        Creates and saves a user with the given email.
        """
        if not email:
            raise ValueError('User must have a email')
        user = self.model(email=email, password=password,
                          first_name=first_name)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password
        """
        user = self.model(email=email)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_moderator = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MainUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=300, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True, db_index=True)
    timestamp = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MainUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '{}: {}'.format(self.full_name, self.email)


class ActivationManager(models.Manager):

    def create(self, email, password, full_name=None):
        activation = self.model(email=email, full_name=full_name)
        activation.password = make_password(password)
        activation.end_time = timezone.now() + timedelta(
            minutes=constants.ACTIVATION_TIME)
        activation.save()
        return activation


class Activation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=300, blank=False, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(blank=True, null=True)
    objects = ActivationManager()

    def is_valid(self, raise_exception=False):
        if self.end_time < timezone.now():
            self.is_active = False
            self.save()
            if raise_exception:
                raise ValidationError(messages.LINK_EXPIRED)
            return False, messages.LINK_EXPIRED
        if not self.is_active:
            if raise_exception:
                raise ValidationError(messages.LINK_INACTIVE)
            return False, messages.LINK_INACTIVE
        return True, None

    def __str__(self):
        return f'{self.email}, {self.is_active}'
