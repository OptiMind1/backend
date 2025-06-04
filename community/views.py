from django.shortcuts import render

from rest_framework import generics, viewsets, filters
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models.signals import post_save
from django.dispatch import receiver
from team.models import Team
from community.models import ChatRoom

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

class PostViewSet(viewsets.ModelViewSet): # type: ignore
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['category'] 
    ordering_fields = ['created_at', 'likes_count']
    ordering = ['-created_at']  # 기본 정렬: 최신순

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        return Post.objects.annotate(
            likes_count=Count('like')
        )

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
@receiver(post_save, sender=Team)
def create_chatroom_for_team(sender, instance, created, **kwargs):
    if created:
        # 이미 채팅방이 없다면 생성
        if not hasattr(instance, 'chatroom'):
            ChatRoom.objects.create(team=instance)