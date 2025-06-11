from django.urls import path
from .views import (
    SubcategoryRolesAPIView,
    MatchingSelectView,
    MatchingRequestCreateAPIView,
)

urlpatterns = [
    # JSON: 세부항목별 추천 역할
    path('roles/', SubcategoryRolesAPIView.as_view(), name='subcategory-roles'),

    # HTML: 팀 매칭 페이지
    path('select/', MatchingSelectView.as_view(), name='matching-select'),

    # JSON: 매칭 요청 저장
    path('request/', MatchingRequestCreateAPIView.as_view(), name='matching-request'),
]
