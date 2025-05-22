from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Profile
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .serializers import (
    ProfileCreateSerializer,
    ProfileUpdateSerializer,
    UserProfileSerializer,
    PublicProfileSerializer
)

# 프로필 검색
class ProfileSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nickname_query = request.query_params.get('nickname', '')
        user = request.user

        if not nickname_query:
            return Response({"error": "닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(nickname=nickname_query)
        except Profile.DoesNotExist:
            return Response({"error": "해당 닉네임을 가진 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        if profile.user == user:
            return Response({"error": "자기 자신의 프로필은 검색할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PublicProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 프로필 등록
class ProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, 'profile'):
            return Response({"error": "프로필이 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProfileCreateSerializer(data=request.data)  # ✅ 여기 변경
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "프로필 등록 성공"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            profile = user.profile  # User -> Profile 연결
        except Profile.DoesNotExist:
            return Response({"error": "프로필이 등록되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return Response({"error": "프로필이 등록되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "프로필 수정 성공"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
