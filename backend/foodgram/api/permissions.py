from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Для внесения изменений требуются права администратора'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin())
        )


class AuthorAdminOrReadOnly(permissions.BasePermission):
    message = 'Внесение изменений доступно только автору и администратору'

    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin())
            or obj.author == request.user
        )
