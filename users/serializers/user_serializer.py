from rest_framework import serializers

from users.models import CustomUser, Subscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


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
