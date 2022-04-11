from datetime import datetime
from random import choices
from string import ascii_letters

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class CarModel(models.Model):
    year = models.IntegerField(default=datetime.today().year)
    model = models.CharField(max_length=150)
    type = models.CharField( max_length=150)

    def __str__(self):
        return self.model


class Link(models.Model):
    original_link = models.URLField()
    shortened_link = models.URLField(blank=True, null=True)

    def shortener(self):
        while True:
            random_string = ''.join(choices(ascii_letters, k=6))
            new_link = settings.HOST_URL + '/' + random_string

            if not Link.objects.filter(shortened_link=new_link).exists():
                break

        return new_link

    def save(self, *args, **kwargs):
        if not self.shortened_link:
            new_link = self.shortener()
            self.shortened_link = new_link
        return super().save(*args, **kwargs)