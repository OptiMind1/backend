from rest_framework import serializers
from .models import Competition

class CompetitionSerializer(serializers.ModelSerializer):
    poster_image = serializers.SerializerMethodField()

    def get_poster_image(self, obj):
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
            'poster_image',    # 프론트 호환용 가짜 필드
            'created_at',
        ]
