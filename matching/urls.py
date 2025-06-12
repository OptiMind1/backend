# urls.py (matching/urls.py)
from django.urls import path
from .views import (
    MatchingRequestCreateAPIView,
    MatchingRequestAcceptAPIView,
    MyMatchingInvitesAPIView,
)

urlpatterns = [
    # 매칭 요청 생성 (팀 + 채팅방 포함)
    path('request/', MatchingRequestCreateAPIView.as_view(), name='matching-request'),

    # 매칭 요청 수락
    path('request/<int:pk>/accept/', MatchingRequestAcceptAPIView.as_view(), name='matching-request-accept'),

    # 내가 받은 초대 목록 조회
    path('my-invites/', MyMatchingInvitesAPIView.as_view(), name='matching-my-invites'),
]
