from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if request.method in ('POST', 'CREATE'):
            return True

        if request.method in ('DELETE',):
            return bool(request.user and request.user.is_staff)

        return False


class UserProPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True