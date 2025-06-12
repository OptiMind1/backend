from django.db import models
from django.conf import settings 

class ChatRoom(models.Model):
    team = models.OneToOneField('team.Team', on_delete=models.CASCADE, related_name='chatroom', null=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_rooms'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom for Team {self.team.id}"
    