from django.contrib import admin
from .models import Post, ChatRoom

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'author', 'Comment')

admin.site.register(ChatRoom)
