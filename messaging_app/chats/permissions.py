from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own messages.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming 'obj' has a 'user' field (ForeignKey to auth.User)
        return obj.user == request.user

