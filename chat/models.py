from django.db import models

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=100, default="default_room")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name