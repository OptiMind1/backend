from rest_framework import serializers
from .models import MatchingRequest
from competition.models import Competition
from users.models import User
from team.models import Team, TeamMember
from community.models import ChatRoom
import uuid

class MatchingRequestSerializer(serializers.ModelSerializer):
    role = serializers.ListField(child=serializers.CharField(), required=False)
    members = serializers.ListField(child=serializers.DictField(), required=False, allow_null=True)
    competition_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MatchingRequest
        fields = ['nationality', 'languages', 'interests', 'in_team', 'desired_partner', 'role', 'members', 'competition_id']

    def create(self, validated_data):
        user = self.context['user']
        nationality = self.context['nationality']
        languages = self.context['languages']
        interests = self.context['interests']
        members = validated_data.pop('members', None)
        competition_id = validated_data.pop('competition_id')

        competition = Competition.objects.get(id=competition_id)

        if members:
            group_id = str(uuid.uuid4())
            team = Team.objects.create(competition=competition)
            chatroom = ChatRoom.objects.create(team=team)
            created_requests = []

            for member in members:
                member_user = user if member['user_id'] == user.user_id else User.objects.get(user_id=member['user_id'])
                profile = getattr(member_user, 'profile', None)
                member_nationality = nationality if member_user == user else getattr(member_user, 'nationality', '')
                member_languages = languages if member_user == user else getattr(profile, 'languages', [])
                member_interests = interests if member_user == user else getattr(profile, 'interests', [])
                role = member.get('role', ['없음'])
                if isinstance(role, str):
                    role = [role]

                req = MatchingRequest.objects.create(
                    user=member_user,
                    nationality=member_nationality,
                    languages=member_languages,
                    interests=member_interests,
                    in_team=True,
                    desired_partner=validated_data.get('desired_partner', ''),
                    role=role,
                    competition=competition,
                    team_group_id=group_id,
                    team=team,
                    is_accepted=(member_user == user)
                )
                created_requests.append(req)

                if member_user == user:
                    TeamMember.objects.create(team=team, user=member_user, role=None)
                    chatroom.members.add(member_user)

            return created_requests

        return MatchingRequest.objects.create(
            user=user,
            nationality=nationality,
            languages=languages,
            interests=interests,
            competition=competition,
            **validated_data
        )
