from rest_framework import serializers

from users.models import CustomUser, Subscription


class UserStatsSerializer(serializers.Serializer):
    articles_count = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    subscriptions_count = serializers.IntegerField(read_only=True)


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username')


class ExtendedBaseUserSerializer(BaseUserSerializer):
    stats = serializers.SerializerMethodField(read_only=True)

    def get_stats(self, obj):
        return UserStatsSerializer(obj).data

    is_subscribed = serializers.BooleanField(read_only=True)
    is_self = serializers.SerializerMethodField(read_only=True)

    def get_is_self(self, obj):
        return self.context.get('request').user == obj

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('is_subscribed', 'is_self', 'stats')


class UserInfoSerializer(ExtendedBaseUserSerializer):
    class Meta(ExtendedBaseUserSerializer.Meta):
        fields = ExtendedBaseUserSerializer.Meta.fields + ('first_name', 'last_name', 'bio', 'date_joined')


class SubscriptionSerializer(serializers.ModelSerializer):
    subscribed_to = BaseUserSerializer(read_only=True)
    subscribed_to_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='subscribed_to',
        write_only=True
    )
    subscriber = BaseUserSerializer(read_only=True)

    subscriber_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='subscriber',
        write_only=True
    )

    class Meta:
        model = Subscription
        fields = ('subscriber', 'subscriber_id', 'subscribed_to', 'subscribed_to_id', 'created_at')
