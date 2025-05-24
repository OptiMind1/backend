from rest_framework import serializers
from .models import MatchingRequest

class MatchingRequestSerializer(serializers.ModelSerializer):
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
        # request.user 로 ForeignKey 채워주기
        return MatchingRequest.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
