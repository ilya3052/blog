from django.urls import path

from notifications.views.notifications_views import SwitchNotificationsModeView, NotificationsView, \
    NotificationsListView

urlpatterns = [
    path('<str:username>/switch/', SwitchNotificationsModeView.as_view(), name='switch-notifications-mode'),
    path('<int:pk>/', NotificationsView.as_view(), name='notification-actions'),
    path('all/', NotificationsListView.as_view(), name='notification-list'),
]