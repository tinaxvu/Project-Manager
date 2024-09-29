from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('common', 'Common User'),
        ('admin', 'PMA ADMIN'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='common')

    def __str__(self):
        return self.username
