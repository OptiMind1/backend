import re
from rest_framework import serializers
from .models import Profile

def validate_nickname(value, current_user=None):
    # 1. 정규식 검사 (한글/영문/숫자만 허용)
    if not re.match(r'^[A-Za-z0-9가-힣]+$', value):
        raise serializers.ValidationError("닉네임에는 공백이나 특수문자를 포함할 수 없습니다.")

    # 2. 중복 검사 (자기 자신의 닉네임은 예외로 허용)
    qs = Profile.objects.filter(nickname=value)
    if current_user:
        qs = qs.exclude(user=current_user)
    if qs.exists():
        raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")

    return value
