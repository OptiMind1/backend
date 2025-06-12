from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet

# Router 설정
router = DefaultRouter()
router.register(r'', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),  # TeamViewSet을 포함시킴
]