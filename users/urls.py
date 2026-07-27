from django.urls import path

from users.views.user_views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='articles-create'),
]