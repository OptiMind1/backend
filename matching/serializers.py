from rest_framework import serializers
from .models import MatchingRequest
from competition.models import Competition
from users.models import User
from team.models import Team, TeamMember
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

            return created_requests

        return MatchingRequest.objects.create(
            user=user,
            nationality=nationality,
            languages=languages,
            interests=interests,
            competition=competition,
            **validated_data
        )


# class MatchingRequestSerializer(serializers.ModelSerializer):
#     nationality = serializers.CharField(read_only=True)
#     languages = serializers.JSONField(read_only=True)
#     interests = serializers.JSONField(read_only=True)
#     role = serializers.ListField(
#         child=serializers.CharField(),
#         required=False  # ✅ 없어도 되게 함
#     )

#     # ✅ 팀 신청용 members 필드 추가
#     members = serializers.ListField(
#         child=serializers.DictField(), required=False, allow_null=True
#     )

#     competition_id = serializers.IntegerField(write_only=True)  # 🔥 추가


#     class Meta:
#         model = MatchingRequest
#         fields = [
#             'nationality',
#             'languages',
#             'interests',
#             'in_team',
#             'desired_partner',
#             'role',
#             'members',
#             'competition_id'
#         ]
    
#     def validate(self, data):
#         in_team = data.get('in_team')
#         role = data.get('role')
#         members = data.get('members')

#         if in_team:
#             if not members:
#                 raise serializers.ValidationError("'in_team=True'일 때는 members 필드가 필요합니다.")
            
#             for member in members:
#                 if 'user_id' not in member:
#                     raise serializers.ValidationError("각 member는 'user_id'를 포함해야 합니다.")
                
#                 # role이 없거나 문자열이면 보정
#                 if 'role' not in member or not member['role']:
#                     member['role'] = ['없음']
#                 elif isinstance(member['role'], str):
#                     member['role'] = [member['role']]

#         else:
#             if not role:
#                 data['role'] = ['없음']
#             elif isinstance(role, str):
#                 data['role'] = [role]

#         return data

#     def create(self, validated_data):
#         user = self.context['user']
#         nationality = self.context['nationality']
#         languages = self.context['languages']
#         interests = self.context['interests']
#         members = validated_data.pop('members', None)

#         # ✅ competition_id 가져오기 (프론트에서 전달해야 함)
#         competition_id = validated_data.pop('competition_id', None)
#         if not competition_id:
#             raise serializers.ValidationError("competition_id 필드는 필수입니다.")
        
#         try:
#             competition = Competition.objects.get(id=competition_id)
#         except Competition.DoesNotExist:
#             raise serializers.ValidationError(f"Competition ID {competition_id}가 존재하지 않습니다.")

#         created_requests = []

#         if members:  # ✅ 팀 신청일 경우
#             group_id = str(uuid.uuid4())  # 고유 그룹 ID 생성

#             for member in members:
#                 try:
#                     if member['user_id'] == user.user_id:
#                         # 본인 처리 (이미 인증된 사용자)
#                         member_user = user
#                         member_nationality = nationality
#                         member_languages = languages
#                         member_interests = interests
#                     else:
#                         # 다른 팀원 처리
#                         member_user = User.objects.get(user_id=member['user_id'])
#                         profile = getattr(member_user, 'profile', None)
#                         member_nationality = getattr(member_user, 'nationality', '')
#                         member_languages = getattr(profile, 'languages', [])
#                         member_interests = getattr(profile, 'interests', [])

#                     req = MatchingRequest.objects.create(
#                         user=member_user,
#                         nationality=member_nationality,
#                         languages=member_languages,
#                         interests=member_interests,
#                         in_team=True,
#                         desired_partner=validated_data.get('desired_partner', ''),
#                         role=member['role'],
#                         competition=competition,
#                         team_group_id= group_id,  # ✅ 여기 추가
#                     )
#                     created_requests.append(req)

#                 except User.DoesNotExist:
#                     raise serializers.ValidationError(f"유저 {member['user_id']}를 찾을 수 없습니다.")
#                 except Exception as e:
#                     raise serializers.ValidationError(f"MatchingRequest 생성 중 오류: {str(e)}")
#             return created_requests  # 리스트 반환 (APIView에서는 무시됨)
        
#         # ✅ 개인 신청일 경우
#         return MatchingRequest.objects.create(
#             user=user,
#             nationality=nationality,
#             languages=languages,
#             interests=interests,
#             competition=competition,  # ✅ 연결
#             **validated_data
#         )
        