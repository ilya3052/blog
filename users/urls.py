from django.urls import path

from users.views.user_views import UserRegistrationView, UserAPIView

urlpatterns = [
    path('me/', UserAPIView.as_view(), name='user-detail'),
    path('register/', UserRegistrationView.as_view(), name='articles-create'),
]