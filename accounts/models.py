"""
    Module contains Custom User Model
    for Django App. it extends the base UserModel
    to make email the mandatory and username field
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
        Custom User Class that overrides the AbstractUser class
        to make email the username field
    """
    username = None
    email = models.EmailField('email address', unique=True, error_messages={
        'unique': "A user with that email already exists.",
    },)
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
