# uni_activities_platform/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views  # views.home 안에 홈뷰가 정의되어 있어야 합니다.

urlpatterns = [
    # 홈 페이지
    path('', views.home, name='home'),

    # 관리자
    path('admin/', admin.site.urls),

    # 사용자 auth
    path('users/', include('users.urls')),

    # 공모전 API
    path('api/competitions/', include('competition.urls')),

    # 팀 API
    path('api/team/', include('team.urls')),

    # 프로필 API
    path('api/profiles/', include('profiles.urls')),

    # 매칭 API 및 UI
    path('api/matching/', include('matching.urls')),
    path('matching/', include('matching.urls')),
]
