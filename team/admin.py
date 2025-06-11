# team/admin.py
from django.contrib import admin
from .models import Team, TeamApplication, TeamMember, CategoryRole

class TeamApplicationInline(admin.TabularInline):
    model = TeamApplication
    extra = 0

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('competition', 'created_at')
    inlines = [TeamApplicationInline, TeamMemberInline]

@admin.register(TeamApplication)
class TeamApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition', 'preferred_team_size', 'submitted_at')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role')

@admin.register(CategoryRole)
class CategoryRoleAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
