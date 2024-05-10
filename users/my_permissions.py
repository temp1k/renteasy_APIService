from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if request.method in ('POST', 'CREATE'):
            return True

        if request.method in ('DELETE',):
            return bool(request.user and request.user.is_staff)

        return True

    def has_object_permission(self, request, view, obj):
        # if request.method == 'PUT':
        #     return bool(obj == request.user or request.user.is_staff)

        return True


class UserChangePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'GET'):
            return bool(obj == request.user or request.user.is_staff)

        return False


class UserProPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
