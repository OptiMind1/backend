from django.contrib import admin
from .models import MatchingRequest

@admin.register(MatchingRequest)
class MatchingRequestAdmin(admin.ModelAdmin):
    list_display  = ('user', 'subcategory', 'role', 'desired_partner', 'in_team', 'created_at')
    list_filter   = ('subcategory', 'role', 'in_team')
    search_fields = ('user__user_id', 'desired_partner')
