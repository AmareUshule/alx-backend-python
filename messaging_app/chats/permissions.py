from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Allow access only to authenticated users who are participants of a conversation.
    Only participants can send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # Check that user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # User must be a participant
        if hasattr(obj, "participants"):
            participants = obj.participants.all()
        elif hasattr(obj, "conversation"):
            participants = obj.conversation.participants.all()
        else:
            return False

        # Allow only if user is a participant
        if request.user not in participants:
            return False

        # Optional: you can explicitly check for methods if ALX requires
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return True

        return False

