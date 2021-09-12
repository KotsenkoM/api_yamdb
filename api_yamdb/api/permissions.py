from rest_framework import permissions
from users.models import UserRoles


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.role == UserRoles.ADMIN
                     or request.user.is_superuser
                     )
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == [UserRoles.ADMIN, UserRoles.MODERATOR]
                or request.user.is_superuser
                )


class ReviewCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        return (request.user.role == [UserRoles.ADMIN, UserRoles.MODERATOR]
                or obj.author == request.user
                )
