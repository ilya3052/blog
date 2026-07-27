from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify, token_blacklist

urlpatterns = [
    path('token/', token_obtain_pair, name='token_obtain_pair'),
    path('token/refresh/', token_refresh, name='token_refresh'),
    path('token/verify/', token_verify, name='token_verify'),
    path('token/blacklist/', token_blacklist, name='token_blacklist'),
]