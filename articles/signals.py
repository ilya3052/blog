import json

from django.dispatch import receiver, Signal
from redis import Redis

from articles.models import Article
from notifications.models import Notifications
from shared.config import Config
from users.models import CustomUser

config = Config.load()
article_published = Signal()

redis_conn = Redis(
    host=config.redis.host,
    port=config.redis.port,
    password=config.secret_redis.password.get_secret_value(),
    encoding="utf-8",
    decode_responses=True
)


@receiver(article_published, sender=Article)
def article_publicated(sender, instance, **kwargs):
    followers = CustomUser.objects.filter(
        subscriptions__subscribed_to=instance.author,
        subscriptions__notifications=True
    )
    article_id = instance.pk
    notifications = Notifications.objects.bulk_create(
        [Notifications(recipient=user, article_id=article_id) for user in followers]
    )
    channel = 'notifications:user'
    for notification in notifications:
        recipient_id = notification.recipient.id
        redis_conn.publish(f'{channel}:{recipient_id}', json.dumps({"recipient_id": recipient_id}))
