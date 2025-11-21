from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name', 'participants__email']

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])
        if not participant_ids or len(participant_ids) < 2:
            return Response(
                {"error": "A conversation must have at least 2 participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name', 'sender__email']

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation_id")
        sender_id = request.data.get("sender_id")
        message_body = request.data.get("message_body", "").strip()

        if not conversation_id or not sender_id or not message_body:
            return Response(
                {"error": "conversation_id, sender_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "Sender not found."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

