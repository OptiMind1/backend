from rest_framework import serializers
from .models import Profile
from users.models import User
from .validators import validate_nickname

# ✅ 프로필 등록용
class ProfileCreateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(validators=[])

    class Meta:
        model = Profile
        fields = [
            'gender',
            'university',
            'academic_year',
            'degree_type',
            'nickname',
            'languages',
            'interests',
            'profile_image'
        ]
        extra_kwargs = {
            'profile_image': {'required': False}  # ✅ 이미지 필드를 optional로 설정
        }

    def validate_nickname(self, value):
        return validate_nickname(value)

# ✅ 프로필 조회용 (User + Profile 통합)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'gender',
            'university',
            'academic_year',
            'degree_type',
            'nickname',
            'languages',
            'interests',
            'profile_image'
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            'user_id',
            'name',
            'birthdate',
            'nationality',
            'phone',
            'email',
            'profile'
        ]

# ✅ 프로필 수정용
class ProfileUpdateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = [
            'university',
            'academic_year',
            'degree_type',
            'nickname',
            'languages',
            'interests',
            'profile_image'
        ]
        extra_kwargs = {
            'nickname': {
                'error_messages': {
                    'unique': '이미 사용 중인 닉네임입니다.'
                }
            },
            'university': {'required': False},
            'academic_year': {'required': False},
            'degree_type': {'required': False},
            'languages': {'required': False},
            'interests': {'required': False},
            'profile_image': {'required': False},
        }

    def validate_nickname(self, value):
        user = self.instance.user
        return validate_nickname(value, current_user=user)
    
class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'nickname',
            'university',
            'degree_type',
            'academic_year',
            'languages',
            'interests',
            'profile_image'
        ]

