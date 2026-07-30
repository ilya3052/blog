from django.urls import path

from notifications.views.notifications_views import SwitchNotificationsModeView

urlpatterns = [
    path('<str:username>/notifications/', SwitchNotificationsModeView.as_view(), name='switch-notifications-mode'),
]