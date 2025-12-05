from rest_framework import permissions

class IsSellerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.scope == "seller"
    