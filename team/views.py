from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Team, TeamApplication, CategoryRole
from .serializers import TeamSerializer, TeamApplicationSerializer
from django.db.models import Count

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """
        팀 신청 처리
        """
        team = self.get_object()
        user = request.user
        role_id = request.data.get('role_id')

        # 이미 신청한 경우 방지
        if TeamApplication.objects.filter(competition=team.competition, user=user).exists():
            return Response({'detail': '이미 이 팀에 신청했습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            role = CategoryRole.objects.get(id=role_id)
        except CategoryRole.DoesNotExist:
            return Response({'detail': '유효하지 않은 역할입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 지원자 정보 입력
        preferred_team_size = request.data.get('preferred_team_size', 4)
        application = TeamApplication.objects.create(
            competition=team.competition,
            user=user,
            preferred_team_size=preferred_team_size
        )
        application.selected_roles.add(role)

        # 추가 필드 업데이트
        application.nationality = request.data.get('nationality', '')
        application.available_languages = request.data.get('available_languages', [])
        application.interests = request.data.get('interests', [])
        application.is_currently_in_team = request.data.get('is_currently_in_team', False)
        application.save()

        return Response({'detail': '팀 신청 완료'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_teams(self, request):
        """
        사용자가 참여한 팀 목록 조회
        """
        user = request.user
        teams = Team.objects.filter(members__user=user).distinct()
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)