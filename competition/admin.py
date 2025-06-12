from django.contrib import admin
from .models import Competition

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'subcategory', 'host', 'deadline', 'created_at', 'image_preview')
    list_filter   = ('category', 'subcategory')
    search_fields = ('title', 'host')
    ordering      = ('category', '-created_at')

    def image_preview(self, obj):
        if obj.image_url:
            return f'<img src="{obj.image_url}" width="60" height="60" style="object-fit:contain;" />'
        return "❌ 없음"
    image_preview.allow_tags = True
    image_preview.short_description = "썸네일"
