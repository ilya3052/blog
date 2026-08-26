from rest_framework import serializers

from articles.models import Article
from notifications.models import Notifications


class NotificationSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(),
    )

    class Meta:
        model = Notifications
        fields = ('id', 'status', 'recipient', 'article', 'publication_date')
