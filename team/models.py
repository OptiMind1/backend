from django.db import models
from django.contrib.auth import get_user_model
from competition.models import Competition

User = get_user_model()

class CategoryRole(models.Model):
    category = models.CharField(max_length=50)  # 예시: "백엔드", "마케팅" 등
    name = models.CharField(max_length=100)    # 역할 이름 (예: 백엔드 개발자, 마케팅 담당자)

    def __str__(self):
        return f"{self.category} - {self.name}"

# 팀 모델
class Team(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.competition.title} 팀 #{self.id}"

# 팀 신청 모델
class TeamApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)  # team 필드 추가
    preferred_team_size = models.PositiveIntegerField(default=4)
    selected_roles = models.ManyToManyField(CategoryRole)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # 추가할 필드들
    nationality = models.CharField(max_length=100, blank=True)
    available_languages = models.JSONField(default=list, blank=True)
    interests = models.JSONField(default=list, blank=True)
    is_currently_in_team = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}의 {self.competition.title} 지원"

# 팀 구성원
class TeamMember(models.Model):
    team = models.ForeignKey(Team, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(CategoryRole, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role}) - 팀 {self.team.id}"