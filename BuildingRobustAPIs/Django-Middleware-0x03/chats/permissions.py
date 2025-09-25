from rest_framework import permissions

class IsAuthenticatedParticipant(permissions.BasePermission):
    """
    Only authenticated users who are participants can access messages.
    """

    def has_object_permission(self, request, view, obj):
        # Check user is authenticated
        if not request.user.is_authenticated:
            return False

        # Safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return request.user in [obj.sender, obj.receiver]

        # Unsafe methods (PUT, PATCH, DELETE)
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in [obj.sender, obj.receiver]

        return False
