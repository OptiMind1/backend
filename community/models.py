from django.db import models
from django.conf import settings  # ✅ 커스텀 유저 모델 지원

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('free', '자유게시판'),
        ('question', '질문게시판'),
        ('review', '후기게시판'),
        ('promo', '홍보게시판'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ 변경됨
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ 변경됨
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # 같은 사용자가 같은 글에 두 번 이상 좋아요 못 누르게 함

    def __str__(self):
        return f"{self.user} likes Post {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ 변경됨
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:20]}"


class ChatRoom(models.Model):
    team = models.OneToOneField('team.Team', on_delete=models.CASCADE, related_name='chatroom', null=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_rooms'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom for Team {self.team.id}"
    