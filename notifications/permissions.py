from rest_framework.permissions import BasePermission

from users.models import CustomUser


class IsItself(BasePermission):
    def has_permission(self, request, view):
        return CustomUser.objects.get(username=view.kwargs['username']) == request.user


class IsNotificationRecipient(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.recipient == request.user
