from django.urls import path
from rest_framework_simplejwt.views import token_refresh, token_verify, token_blacklist

from social_auth.views.auth_views import UserRegistrationView, cookie_token_obtain_pair

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='articles-create'),

    path('token/', cookie_token_obtain_pair, name='token_obtain_pair'),
    path('token/refresh/', token_refresh, name='token_refresh'),
    path('token/verify/', token_verify, name='token_verify'),
    path('token/blacklist/', token_blacklist, name='token_blacklist'),
]