from rest_framework import permissions


ADMIN_PERMISSION_MESSAGE = 'Для внесения изменений требуются права администратора'
AUTHOR_ADMIN_PERMISSION_MESSAGE = 'Внесение изменений доступно только автору и администратору'


class IsAdminOrReadOnly(permissions.BasePermission):
    message = ADMIN_PERMISSION_MESSAGE

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin())
        )


class AuthorAdminOrReadOnly(permissions.BasePermission):
    message = AUTHOR_ADMIN_PERMISSION_MESSAGE

    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin())
            or obj.author == request.user
        )
