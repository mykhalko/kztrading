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
        self.create_user(email, password, name, surname, phone_number,
                         is_active=True, is_staff=True, is_admin=True)


class User(AbstractBaseUser):

    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=32, null=True)
    registration_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff')
    is_admin = models.BooleanField(default=False, verbose_name='admin')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)
