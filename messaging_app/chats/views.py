from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

# -----------------------------------
# Conversation ViewSet
# -----------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer

    # Override create to allow adding participants by ID
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


# -----------------------------------
# Message ViewSet
# -----------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer

    # Override create to link to conversation and sender
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

