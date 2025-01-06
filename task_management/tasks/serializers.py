from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "created_at",
            "updated_at",
            "user",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user"]
