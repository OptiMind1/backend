from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Competition
from .serializers import CompetitionSerializer
from .crawler import save_allcon_to_db
from .utils import classify_category
from .crawler import fetch_competition_detail_page

from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication



# 기존에 누락된 CompetitionListView, CompetitionDetailView 추가

class CompetitionListView(generics.ListAPIView):
    """
    API: 공모전 전체 조회
    """
    permission_classes = [AllowAny]
    queryset = Competition.objects.all().order_by('-created_at')
    serializer_class = CompetitionSerializer

class CompetitionDetailView(generics.RetrieveAPIView):
    """
    API: 공모전 상세 조회
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]  # ✅ 여기에 명시적으로 추가!
    authentication_classes = []



class CrawlAndSaveAllconAPI(APIView):
    """
    API: Allcon 크롤링해서 DB에 저장
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]

    def get(self, request):
        saved_count = save_allcon_to_db()  # ✅ 여기로 변경
        return Response(
            {'message': f'{saved_count}개 저장됨'},
            status=status.HTTP_200_OK
        )


class FetchAllconDetailAPI(APIView):
    """
    예) GET /api/competition/crawl/detail/?url=/view/contest/520261
    """
    permission_classes = [AllowAny]

    def get(self, request):
        url = request.query_params.get("url")
        if not url:
            return Response({"error": "url 파라미터가 필요합니다"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = fetch_competition_detail_page(url)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            # 내부에서 뭔가 예외가 터지면 500과 함께 에러 메시지를 내려준다.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)