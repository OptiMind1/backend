# views.py (matching/views.py)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import MatchingRequest
from team.models import Team, TeamMember
from chat.models import ChatRoom
from competition.models import Competition
from users.models import User
import uuid

class MatchingRequestCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request):
        user = request.user
        data = request.data

        members = data.get("members", [])
        competition_id = data.get("competition_id")
        desired_partner = data.get("desired_partner", "")

        if not competition_id:
            return Response({"error": "competition_id는 필수입니다."}, status=400)

        try:
            competition = Competition.objects.get(id=competition_id)
        except Competition.DoesNotExist:
            return Response({"error": "유효하지 않은 competition_id입니다."}, status=404)

        group_id = str(uuid.uuid4())
        team = Team.objects.create(competition=competition)
        chatroom = ChatRoom.objects.create(team=team)

        created_requests = []

        for member in members:
            try:
                user_id = member['user_id']
                role = member.get('role', ['없음'])
                if isinstance(role, str):
                    role = [role]

                member_user = user if user.user_id == user_id else User.objects.get(user_id=user_id)
                profile = getattr(member_user, 'profile', None)
                nationality = getattr(member_user, 'nationality', '')
                languages = getattr(profile, 'languages', [])
                interests = getattr(profile, 'interests', [])

                matching_request = MatchingRequest.objects.create(
                    user=member_user,
                    nationality=nationality,
                    languages=languages,
                    interests=interests,
                    in_team=True,
                    desired_partner=desired_partner,
                    role=role,
                    competition=competition,
                    team_group_id=group_id,
                    team=team,
                    is_accepted=(member_user == user)
                )
                created_requests.append(matching_request)

                if member_user == user:
                    TeamMember.objects.create(team=team, user=member_user, role=None)
                    chatroom.members.add(member_user)

            except User.DoesNotExist:
                return Response({"error": f"유저 {member['user_id']}를 찾을 수 없습니다."}, status=400)

        return Response({
            "message": "팀과 채팅방이 생성되었고 요청이 전송되었습니다.",
            "team_id": team.id,
            "chatroom_id": chatroom.id,
            "requests": [r.id for r in created_requests]
        }, status=201)

class MatchingRequestAcceptAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request, pk):
        matching_request = get_object_or_404(MatchingRequest, pk=pk, user=request.user)

        if matching_request.is_accepted:
            return Response({"message": "이미 수락된 요청입니다."}, status=400)

        matching_request.is_accepted = True
        matching_request.save()

        TeamMember.objects.create(team=matching_request.team, user=request.user, role=None)
        chatroom = matching_request.team.chatroom
        chatroom.members.add(request.user)

        return Response({
            "message": "팀 요청을 수락했습니다.",
            "team_id": matching_request.team.id
        }, status=200)

class MyMatchingInvitesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user

        invites = MatchingRequest.objects.filter(
            user=user,
            in_team=True,
            is_accepted=False,
            team__isnull=False
        ).select_related('team', 'competition')

        result = [
            {
                "matching_id": invite.id,
                "team_id": invite.team.id,
                "team_name": str(invite.team),
                "competition_title": invite.competition.title,
                "requested_at": invite.created_at
            }
            for invite in invites
        ]

        return Response(result, status=200)
