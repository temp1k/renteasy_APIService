from rest_framework import permissions


class HousingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'retrieve':
            return request.user.has_perms('fix_list_perm')
        if view.action == 'update' or view.action == 'partial_update':
            return request.user.has_perms('fix_an_appointment')
        if view.action == 'destroy':
            return request.user.has_perms('fix_an_appointment')
        if view.action == 'create':
            return request.user.has_perms('fix_an_appointment')

        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        print(request.user)
        if request.method in ('PUT', 'CREATE', 'POST', 'DELETE'):
            return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.method == 'PUT':
            return obj.owner == request.user

        return False
