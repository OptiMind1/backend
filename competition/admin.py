from django.contrib import admin
from .models import Competition

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display  = ('title','category','subcategory','host','deadline','created_at')
    list_filter   = ('category','subcategory')   # 이제 subcategory 필터가 제대로 동작합니다
    search_fields = ('title','host')
    ordering      = ('category','-created_at')
