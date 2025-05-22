from rest_framework import serializers
from .models import User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'email', 'password', 'name', 'birthdate', 'nationality', 'phone']
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'unique': '이미 가입된 이메일입니다.'
                }
            },
            'user_id': {
                'error_messages': {
                    'unique': '이미 사용 중인 ID입니다.'
                }
            }
        }

    def create(self, validated_data):
        # UserManager.create_user를 사용해서 password를 hashing하고 저장합니다
        return User.objects.create_user(**validated_data)
