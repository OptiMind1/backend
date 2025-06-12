from django.shortcuts import render
from django.dispatch import receiver
from team.models import Team
from chat.models import ChatRoom
from django.db.models.signals import post_save

@receiver(post_save, sender=Team)
def create_chatroom_for_team(sender, instance, created, **kwargs):
    if created:
        # 이미 채팅방이 없다면 생성
        if not hasattr(instance, 'chatroom'):
            ChatRoom.objects.create(team=instance)