from django.db import models
from django.conf import settings

class MatchingRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matching_requests"
    )
    nationality     = models.CharField(max_length=50)
    languages       = models.JSONField(default=list)   # ["English", "Korean"]
    interests       = models.JSONField(default=list)   # ["영상", "마케팅"]
    in_team         = models.BooleanField(default=False)
    desired_partner = models.CharField(
        max_length=30,
        blank=True,
        help_text="함께 팀을 하고 싶은 사람의 user_id"
    )
    subcategory     = models.CharField(max_length=50)
    role            = models.CharField(max_length=50)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_id} → {self.subcategory}/{self.role}"
