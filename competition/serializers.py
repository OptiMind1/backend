from rest_framework import serializers
from .models import Competition

class CompetitionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.image_url

    class Meta:
        model = Competition
        fields = [
            'id',
            'title',
            'category',
            'subcategory',
            'host',
            'description',
            'deadline',
            'link',
            # 'poster_image',    # 프론트 호환용 가짜 필드
            'image_url',
            'created_at',
        ]