from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем своего профиля.
    Пользователь может редактировать/удалять только свой профиль.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or obj.id == request.user.id
