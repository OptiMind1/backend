# community/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ChatRoom
from team.models import Team 

@receiver(post_save, sender=Team)
def create_chatroom_for_team(sender, instance, created, **kwargs):
    if created:
        # 팀 생성 시 ChatRoom이 자동 생성됨
        ChatRoom.objects.create(team=instance)
