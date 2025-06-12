# users/signals.py

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def remove_user_related_data(sender, instance, **kwargs):
    # ✅ ChatRoom.members 에서 제거
    if hasattr(instance, 'chat_rooms'):
        for room in instance.chat_rooms.all():
            room.members.remove(instance)