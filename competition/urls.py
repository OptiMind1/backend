# backend/competition/urls.py

from django.urls import path
from .views import (
    CompetitionListView,
    CompetitionDetailView,
    CrawlAndSaveAllconAPI,
    FetchAllconDetailAPI,   # “상세 크롤링” 뷰
)

urlpatterns = [
    # 1) 공모전 전체 조회
    path('', CompetitionListView.as_view(), name='competition-list'),
    # 2) 공모전 단건 상세 조회
    path('<int:id>/', CompetitionDetailView.as_view(), name='competition-detail'),

    # 3) All-Con 전체 크롤링 & 저장
    path('crawl/allcon/', CrawlAndSaveAllconAPI.as_view(), name='crawl_allcon'),
    # 4) All-Con 상세 정보 (포스터+본문HTML) 크롤링
    path('crawl/detail/', FetchAllconDetailAPI.as_view(), name='crawl_allcon_detail'),
]
