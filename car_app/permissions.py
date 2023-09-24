from rest_framework import permissions

class ReadOnlyOrAuthenticated(permissions.BasePermission):
    """
    Custom permission class that allows read-only access to unauthenticated users
    but requires authentication for write (PUT, PATCH, DELETE) operations.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and not request.user.is_authenticated:
            return True
        return request.user and request.user.is_authenticated