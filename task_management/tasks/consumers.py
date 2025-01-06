import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .serializers import TaskSerializer
from channels.layers import get_channel_layer
from .models import Task


class TaskStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        json.loads(text_data)
        await self.send(text_data=json.dumps({"message": "Message received"}))

    @database_sync_to_async
    def serialize_task(self, task):
        return TaskSerializer(task).data

    async def task_status_update(self, event):
        task_data = event["task_data"]
        await self.send(text_data=json.dumps({"task": task_data}))


@database_sync_to_async
def notify_task_status_change(task_id):
    channel_layer = get_channel_layer()
    task = Task.objects.get(id=task_id)
    serialized_task = TaskSerializer(task).data

    group_name = f"user_{task.user.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "task_status_update",
            "task_data": serialized_task,
        },
    )
