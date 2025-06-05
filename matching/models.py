from django.db import models
from django.conf import settings
from competition.models import Competition  # ← 공모전 모델 import


class MatchingRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matching_requests"
    )
    nationality     = models.CharField(max_length=50)
    languages       = models.JSONField(default=list)   # e.g. ["Korean","English"]
    interests       = models.JSONField(default=list)   # e.g. ["아이디어","마케팅"]
    in_team         = models.BooleanField(default=False)
    desired_partner = models.CharField(
        max_length=30,
        blank=True,
        help_text="함께 팀을 하고 싶은 사람의 user_id"
    )
    role = models.JSONField(default=list)  # ✅ 여러 역할을 리스트로 저장    
    created_at      = models.DateTimeField(auto_now_add=True)

    # ✅ 팀 신청 시 같은 그룹으로 묶을 수 있도록 team_group_id 필드 추가
    team_group_id = models.CharField(max_length=64, blank=True, null=True)
    
    # 실제 team 앱이랑 연결
    team = models.ForeignKey("team.Team", on_delete=models.SET_NULL, null=True, blank=True, related_name="matched_requests")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matching_requests')

    def __str__(self):
        return f"{self.user.user_id} → {self.role}"
    


