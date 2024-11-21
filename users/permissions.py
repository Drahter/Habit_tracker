from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Только те, кто создавал объекты, могут с ними взаимодействовать.
    """

    def has_object_permission(self, request, view, obj):
        if obj.created_by == request.user:
            return True
        return False


class IsPublic(permissions.BasePermission):
    """
    Только те, кто создавал объекты, могут с ними взаимодействовать.
    """

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return False
