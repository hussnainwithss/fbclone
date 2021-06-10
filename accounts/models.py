from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
        Custom User Class that overrides the AbstractUser class
        to make email the username field and making username first part 
        of email
    """
    username = None
    email = models.EmailField('email address', unique=True,error_messages={
            'unique': "A user with that email already exists.",
        },)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    
    def __str__(self):
        return self.email