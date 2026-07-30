from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notifications
from notifications.serializers.notifications_serializers import NotificationSerializer
from users.models import CustomUser, Subscription


class NotificationsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notifications.objects.all()


class NotificationsListView(generics.ListAPIView):
    def get_queryset(self):
        username = self.kwargs['username']
        user_id = CustomUser.objects.get(username=username).pk
        return Notifications.objects.filter(recipient_id=user_id)

    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notifications.objects.all()


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
