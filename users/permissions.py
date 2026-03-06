from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем своего профиля.
    Пользователь может редактировать/удалять только свой профиль.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or obj.id == request.user.id


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение: только владелец может редактировать свою привычку."""
    def has_object_permission(self, request, view, obj):
        """Проверяет права доступа к объекту."""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user
