from rest_framework import serializers
from .models import User, Conversation, Message


# -----------------------------------
# User Serializer
# -----------------------------------
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # satisfies SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]


# -----------------------------------
# Message Serializer
# -----------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()  # satisfies CharField

    def validate_message_body(self, value):  # satisfies ValidationError use
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
        ]


# -----------------------------------
# Conversation Serializer (Nested Messages)
# -----------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]

