from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser, Subscription
from users.serializers.user_serializer import UserSerializer, SubscriptionSerializer


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionView(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        username = self.kwargs['username']
        subscribed_to_id = CustomUser.objects.get(username=username).pk
        request.data['subscribed_to_id'] = subscribed_to_id
        request.data['subscriber_id'] = request.user.id
        instance = Subscription.objects.filter(
            subscribed_to_id=subscribed_to_id,
            subscriber_id=request.user.id
        )
        if instance.first():
            instance.delete()
            return Response({"detail": "Подписка удалена"}, status=status.HTTP_204_NO_CONTENT)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        user = CustomUser.objects.get(username=username)

        followers = CustomUser.objects.filter(
            id__in=user.subscribers.values('subscriber_id')
        )
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class MySubscriptionsView(generics.ListAPIView):
    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(
            id__in=user.subscriptions.values('subscribed_to_id')
        )

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class SwitchNotificationsModeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        username = self.kwargs['username']
        subscribed_to_id = CustomUser.objects.get(username=username).pk
        subscription = Subscription.objects.filter(
            subscribed_to_id=subscribed_to_id,
            subscriber_id=request.user.id
        ).first()
        if subscription:
            subscription.notifications = not subscription.notifications
            subscription.save()
            return Response({"detail": "Режим уведомлений изменен"}, status=status.HTTP_200_OK)
        return Response({"detail": "Подписка не найдена"}, status=status.HTTP_404_NOT_FOUND)