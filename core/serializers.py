from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "author", "text", "created_at", "likes_count"]
