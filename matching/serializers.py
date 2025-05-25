from rest_framework import serializers
from .models import MatchingRequest

class MatchingRequestSerializer(serializers.ModelSerializer):
    
    nationality = serializers.CharField(read_only=True)
    languages = serializers.JSONField(read_only=True)
    interests = serializers.JSONField(read_only=True)

    class Meta:
        model = MatchingRequest
        fields = [
            'nationality',
            'languages',
            'interests',
            'in_team',
            'desired_partner',
            'subcategory',
            'role'
        ]

    def create(self, validated_data):
        user = validated_data.pop('user')
        nationality = self.context.get('nationality')
        languages = self.context.get('languages')
        interests = self.context.get('interests')

        # interests 중복 방지
        validated_data.pop('interests', None)


        return MatchingRequest.objects.create(
            user=user,
            nationality=nationality,
            languages=languages,
            interests=interests,
            **validated_data
        )