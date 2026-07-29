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
        following_id = (CustomUser.objects.get(username=username)).pk
        request.data['following_id'] = following_id
        request.data['follower_id'] = request.user.id
        if (instance := Subscription.objects.filter(following_id=following_id, follower_id=request.user.id)).exists():
            instance.delete()
            return Response({"detail": "Подписка удалена"}, status=status.HTTP_204_NO_CONTENT)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        user = CustomUser.objects.get(username=username)

        followers = CustomUser.objects.filter(
            id__in=user.followers.values('follower_id')  # берет подписчиков user-а и вытаскивает у них id
        )
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class MySubscriptionsView(generics.ListAPIView):
    def get_queryset(self):
        user = self.request.user
        # user.following - на кого подписан текущий пользователь
        followers = CustomUser.objects.filter(
            id__in=user.following.values('following_id')
        )
        return followers

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
