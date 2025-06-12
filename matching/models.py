from django.db import models
from django.conf import settings
from competition.models import Competition
from team.models import Team

class MatchingRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="matching_requests")
    nationality = models.CharField(max_length=50)
    languages = models.JSONField(default=list)
    interests = models.JSONField(default=list)
    in_team = models.BooleanField(default=False)
    desired_partner = models.CharField(max_length=30, blank=True)
    role = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    team_group_id = models.CharField(max_length=64, blank=True, null=True)
    team = models.ForeignKey("team.Team", on_delete=models.SET_NULL, null=True, blank=True, related_name="matched_requests")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matching_requests')
    is_accepted = models.BooleanField(default=False)  # <- 수락 여부