from django.db.models.signals import post_save
from django.dispatch import receiver

from articles.models import Article
from notifications.models import Notifications
from users.models import CustomUser


@receiver(post_save, sender=Article)
def article_publicated(sender, instance, created, **kwargs):
    followers = CustomUser.objects.filter(
        subscriptions__subscribed_to=instance.author,
        subscriptions__notifications=True
    )
    notify_instances = Notifications.objects.bulk_create(
        [Notifications(recipient=user, article=instance) for user in followers]
    )
    # TODO: передача уведомлений в redis для отправки через sse
