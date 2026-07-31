from django.urls import path

from users.views.user_views import PublicUserInfoView, SubscriptionView, MySubscriptionsView, UserInfoView

urlpatterns = [
    path('me/', UserInfoView.as_view(), name='me'),
    path('subscriptions/my/', MySubscriptionsView.as_view(), name='my-followers'),
    path('<str:username>/followers/', SubscriptionView.as_view(), name='user-followers'),
    path('<str:username>/', PublicUserInfoView.as_view(), name='user-detail'),
]
