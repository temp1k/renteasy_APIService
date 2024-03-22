from rest_framework import permissions


class HousingPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True

        if request.method in ('POST', 'CREATE'):
            return True

        if request.method in ('DELETE', 'GET'):
            return bool(request.user and request.user.is_staff)

        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        return obj == request.user

        return False


class PublishedHousingPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.housing.owner:
            return True

        if request.method in ('POST', 'CREATE'):
            return bool(request.user.is_authenticated)

        if request.method == 'GET':
            return True

        if request.method in ('DELETE', 'PUT'):
            return bool(request.user and request.user.is_staff)

        return False


class IsAuthenticatedPostIsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('POST', 'CREATE'):
            return bool(request.user.is_authenticated)

        if request.method == 'DELETE':
            return bool(request.user and request.user.is_staff)

        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('PUT', 'CREATE', 'POST', 'DELETE'):
            return bool(request.user and request.user.is_staff)


class IsAuthenticatedOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('PUT', 'DELETE'):
            return bool(request.user and request.user.is_staff)

        if request.method in ('POST', 'CREATE'):
            return bool(request.user.is_authenticated)

        if request.method == 'GET':
            return True

        return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('POST', 'CREATE'):
            return True

        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user

        return False


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
