from rest_framework import serializers

from articles.seriaizers.articles_serializers import ArticleSerializer
from notifications.models import Notifications


class NotificationSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    class Meta:
        model = Notifications
        fields = ('id', 'status', 'recipient', 'article', 'publication_date')