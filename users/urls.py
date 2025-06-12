from django.urls import path
from .views import SignupView, CheckEmailView, CheckIdView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 회원가입
    path('signup/', SignupView.as_view(), name='signup'),
    # 로그인(JWT 발급)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 리프레시 토큰
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 중복 검사
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
    path('check_id/',    CheckIdView.as_view(),    name='check_id'),
]