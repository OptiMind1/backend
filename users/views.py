from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status, permissions
from .serializers import SignupSerializer
from .models import User

# 이메일 중복 체크
class CheckEmailView(APIView):
    def get(self, request):
        email = request.query_params.get('email', '')
        if not email:
            return Response({'error': '이메일을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'is_duplicate': True, 'message': '이미 가입된 이메일입니다.'})
        return Response({'is_duplicate': False, 'message': '사용 가능한 이메일입니다.'})

# 사용자 아이디 중복 체크
class CheckIdView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id', '')
        if not user_id:
            return Response({'error': '아이디를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(user_id=user_id).exists():
            return Response({'is_duplicate': True, 'message': '이미 사용 중인 ID입니다.'})
        return Response({'is_duplicate': False, 'message': '사용 가능한 ID입니다.'})

# 회원가입 처리
class SignupView(APIView):
    authentication_classes = [] 
    permission_classes = [permissions.AllowAny]    # ← 여기 추가

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)