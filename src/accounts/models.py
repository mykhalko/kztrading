import datetime
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password, name, surname, phone_number,
                    is_active=None, is_staff=None, is_admin=None):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.name = name
        user.surname = surname
        user.phone_number = phone_number
        user.is_active = is_active
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, name=None, surname=None, phone_number=None):
        self.create_user(email, password, name, surname, is_active=True, is_staff=True)

    def create_superuser(self, email, password, name=None, surname=None, phone_number=None):
        user = self.create_user(email, password, name, surname, phone_number,
                         is_active=True, is_staff=True, is_admin=True)
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=32, null=True)
    registration_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff')
    is_admin = models.BooleanField(default=False, verbose_name='admin')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)


class ConfirmationManager(models.Manager):

    def create_confirmation_link(self, user):
        if not user:
            raise ValueError('Can\'t create confirmation link with no linked user!')
        if user.is_active:
            raise ValueError('User email {} already confirmed!'.format(user.email))
        confirmation = self.model(user=user)
        confirmation.save(using=self._db)
        return confirmation

def get_expiration_time():
    return timezone.now() + datetime.timedelta(days=1)

class Confirmation(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expiration = models.DateTimeField(default=get_expiration_time())
    visited = models.BooleanField(default=False)

    objects = ConfirmationManager()

    def __str__(self):
        return str(self.user) + ' ' +  str(self.id)
