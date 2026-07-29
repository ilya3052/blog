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


class Subscription(models.Model):
    pk = models.CompositePrimaryKey('following_id', 'follower_id')
    # user.followers - кто подписан на user
    # user.following - на кого подписан user
    following = models.ForeignKey('CustomUser', on_delete=models.CASCADE,
                                  related_name='followers')  # тот на кого подписались
    follower = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='following')  # кто подписался
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subscriptions'
        indexes = [
            models.Index(fields=['follower']),
        ]
