from rest_framework import permissions

class IsRider(permissions.BasePermission):

    def has_permission(self, request, view):
        print("it hit this endpoint rider")
        return request.user.is_authenticated and request.user.user_type == 'rider'


class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        print("it hit this endpoint customer")
        return request.user.user_type in ['customer', 'vendor']


class IsNotificationOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.account == request.user