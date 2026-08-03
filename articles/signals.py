import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from redis import Redis

from articles.models import Article
from notifications.models import Notifications
from shared.config import Config
from users.models import CustomUser

config = Config.load()

redis_conn = Redis(
    host=config.redis.host,
    port=config.redis.port,
    password=config.secret_redis.password.get_secret_value(),
    encoding="utf-8",
    decode_responses=True
)


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
    channel = 'notifications:new'
    print(notify_instances[0].recipient.id)
    res = redis_conn.publish(channel, json.dumps({"recipient_id": notify_instances[0].recipient.id}))
    print(res)
        # redis_conn.publish(channel, json.dumps(
        # ({"recipient_id": notify_instance.recipient, "article_id": instance.id}) for notify_instance in
        # notify_instances))
