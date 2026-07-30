from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser, Subscription


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
