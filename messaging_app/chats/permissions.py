from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Allow access only to users who are participants of a conversation.
    """

    def has_object_permission(self, request, view, obj):
        """
        For Conversation objects: check if user is a participant.
        For Message objects: check if user is sender OR participant.
        """

        # Case 1: obj is a Conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Case 2: obj is a Message
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False

