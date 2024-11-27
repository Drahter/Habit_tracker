from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Только те, кто создавал объекты, могут с ними взаимодействовать.
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
