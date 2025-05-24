from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .models import Competition
from .serializers import CompetitionSerializer
from .crawler import fetch_allcon_competitions
from .utils import classify_category

# 기존에 누락된 CompetitionListView, CompetitionDetailView 추가

class CompetitionListView(generics.ListAPIView):
    """
    API: 공모전 전체 조회
    """
    queryset = Competition.objects.all().order_by('-created_at')
    serializer_class = CompetitionSerializer

class CompetitionDetailView(generics.RetrieveAPIView):
    """
    API: 공모전 상세 조회
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    lookup_field = 'id'


class CrawlAndSaveAllconAPI(APIView):
    """
    API: Allcon 크롤링해서 DB에 저장
    """
    renderer_classes = [JSONRenderer]

    def get(self, request):
        entries = fetch_allcon_competitions()
        saved_count = 0

        for entry in entries:
            title       = entry['title']
            raw_cate    = entry['category']
            deadline    = entry.get('deadline')
            link        = entry.get('link', '')
            description = entry.get('description', '')

            category = classify_category(raw_cate)

            if not Competition.objects.filter(title=title).exists():
                Competition.objects.create(
                    title=       title,
                    category=    category,
                    host=        '',          # 필요 시 크롤링 추가
                    description= description,
                    deadline=    deadline,
                    link=        link
                )
                saved_count += 1

        return Response(
            {'message': f'{saved_count}개 저장됨'},
            status=status.HTTP_200_OK
        )
