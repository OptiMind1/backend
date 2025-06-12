from django.contrib import admin
from .models import MatchingRequest

@admin.register(MatchingRequest)
class MatchingRequestAdmin(admin.ModelAdmin):
    list_display  = (
        'user', 'role', 'desired_partner', 'in_team',
        'team_group_id',
        'team', 'competition','competition_id','created_at')
    list_filter   = ('role', 'in_team')
    search_fields = ('user__user_id', 'desired_partner', 'team__id', 'competition__title')
