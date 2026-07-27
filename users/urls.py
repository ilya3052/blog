from django.urls import path

from users.views.user_views import UserAPIView

urlpatterns = [
    path('me/', UserAPIView.as_view(), name='user-detail'),
]
