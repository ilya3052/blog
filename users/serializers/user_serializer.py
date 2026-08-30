from django.db import connection
from rest_framework import serializers

from users.models import CustomUser, Subscription


class UserStatsSerializer(serializers.Serializer):
    articles_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    subscribers_count = serializers.SerializerMethodField(read_only=True)
    subscriptions_count = serializers.SerializerMethodField(read_only=True)

    def get_articles_count(self, obj):
        return obj.articles.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    def get_subscriptions_count(self, obj):
        return obj.subscriptions.count()


class UserSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField(read_only=True)
    is_self = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.BooleanField(read_only=True)

    def get_stats(self, obj):
        return UserStatsSerializer(obj).data

    def get_is_self(self, obj):
        return self.context.get('request').user == obj

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'date_joined', 'stats', 'is_self',
                  'is_subscribed')


class SubscriptionSerializer(serializers.ModelSerializer):
    subscribed_to = UserSerializer(read_only=True)
    subscribed_to_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='subscribed_to',
        write_only=True
    )
    subscriber = UserSerializer(read_only=True)

    subscriber_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='subscriber',
        write_only=True
    )

    class Meta:
        model = Subscription
        fields = ('subscriber', 'subscriber_id', 'subscribed_to', 'subscribed_to_id', 'created_at')
