from django.urls import path

from users.views.user_views import UserAPIView, SubscriptionView, MySubscriptionsView

urlpatterns = [
    path('subscriptions/my/', MySubscriptionsView.as_view(), name='my-followers'),
    path('<str:username>/followers/', SubscriptionView.as_view(), name='user-followers'),
    path('<str:username>/', UserAPIView.as_view(), name='user-detail')
]
