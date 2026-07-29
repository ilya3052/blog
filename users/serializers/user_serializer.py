from rest_framework import serializers

from users.models import CustomUser, Subscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class SubscriptionSerializer(serializers.ModelSerializer):
    following = UserSerializer(read_only=True)
    following_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='following',
        write_only=True
    )
    follower = UserSerializer(read_only=True)

    follower_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='follower',
        write_only=True
    )

    class Meta:
        model = Subscription
        fields = ('follower', 'follower_id', 'following', 'following_id', 'created_at')
