from django.urls import path
from .views import (
    CompetitionListView,
    CompetitionDetailView,
    CrawlAndSaveAllconAPI,
)

urlpatterns = [
    # 리스트 / 상세
    path('', CompetitionListView.as_view(), name='competition-list'),
    path('<int:id>/', CompetitionDetailView.as_view(), name='competition-detail'),


    # Allcon 크롤링 및 저장
    path('crawl/allcon/', CrawlAndSaveAllconAPI.as_view(), name='crawl_allcon'),
]
