from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True, blank=False, null=False)
    REQUIRED_FIELDS = ['username']
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username']),
        ]