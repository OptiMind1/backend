from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'user', 'university', 'degree_type', 'academic_year']
    search_fields = ['nickname', 'user__user_id']  # 이거 추가하면 검색됨
