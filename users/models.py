from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)

    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username']),
        ]


class Subscription(models.Model):
    pk = models.CompositePrimaryKey('subscribed_to_id', 'subscriber_id')
    subscribed_to = models.ForeignKey('CustomUser', on_delete=models.CASCADE,
                                  related_name='subscribers')  # тот на кого подписались
    subscriber = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='subscriptions')  # кто подписался
    created_at = models.DateTimeField(auto_now_add=True)
    notifications = models.BooleanField(default=True)
    class Meta:
        db_table = 'subscriptions'
        indexes = [
            models.Index(fields=['subscriber']),
        ]
