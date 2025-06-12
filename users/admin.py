from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from .models import User

# 관련 모델 import
from profiles.models import Profile
from matching.models import MatchingRequest
from team.models import TeamApplication, TeamMember
from community.models import Post, Comment, Like

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'email', 'name', 'birthdate', 'nationality', 'is_staff']
    actions = ['safe_delete_users']  # ✅ 커스텀 액션 등록

    @admin.action(description="선택한 유저 안전 삭제 (연관 정보 포함)")
    def safe_delete_users(self, request, queryset):
        for user in queryset:
            try:
                with transaction.atomic():
                    Profile.objects.filter(user=user).delete()
                    MatchingRequest.objects.filter(user=user).delete()
                    TeamApplication.objects.filter(user=user).delete()
                    TeamMember.objects.filter(user=user).delete()
                    Post.objects.filter(author=user).delete()
                    Comment.objects.filter(author=user).delete()
                    Like.objects.filter(user=user).delete()

                    for room in user.chat_rooms.all():
                        room.members.remove(user)

                    user.delete()

                    self.message_user(request, f"[{user.user_id}] 삭제 완료", messages.SUCCESS)

            except Exception as e:
                self.message_user(request, f"[{user.user_id}] 삭제 실패: {str(e)}", messages.ERROR)