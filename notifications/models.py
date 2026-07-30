from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Notifications(models.Model):
    STATUS = {"UNREAD": "UNREAD", "READ": "READ"}
    recipient = models.ForeignKey(user, on_delete=models.CASCADE, related_name='notifications')
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, related_name='notifications')
    status = models.CharField(choices=STATUS.items(), max_length=6, default=STATUS["UNREAD"])
    publication_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
