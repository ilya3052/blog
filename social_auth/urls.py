from django.urls import path

from social_auth.views.auth_views import UserRegistrationView, cookie_token_obtain_pair, cookie_token_refresh, \
    cookie_token_verify, cookie_token_blacklist

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='articles-create'),

    path('token/', cookie_token_obtain_pair, name='token_obtain_pair'),
    path('token/refresh/', cookie_token_refresh, name='token_refresh'),
    path('token/verify/', cookie_token_verify, name='token_verify'),
    path('token/blacklist/', cookie_token_blacklist, name='token_blacklist'),
]
