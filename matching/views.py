from django.views.generic import TemplateView
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import MatchingRequest
from .serializers import MatchingRequestSerializer
from .constants import SUBCATEGORY_ROLES

class SubcategoryRolesAPIView(APIView):
    """
    GET /api/matching/roles/?subcategory=슬로건
    → {"roles": [...]}
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        sub = request.query_params.get('subcategory')
        if not sub:
            return Response({'error': 'subcategory 파라미터를 보내주세요.'}, status=400)
        roles = SUBCATEGORY_ROLES.get(sub)
        if roles is None:
            return Response({'error': f'알 수 없는 subcategory: {sub}'}, status=400)
        return Response({'roles': roles})

class MatchingSelectView(TemplateView):
    """
    GET /matching/select/
    → matching/templates/matching/select.html 렌더링
    """
    template_name = "matching/select.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['subcategories'] = [
            '창업','아이디어','슬로건','네이밍','마케팅',
            '사진','영상',
            '포스터','로고','상품','캐릭터','그림','웹툰','광고','도시건',
            '논문','수기','시','시나리오','공학','과학',
            '음악','댄스','e스포츠'
        ]
        return ctx

class MatchingRequestCreateAPIView(generics.CreateAPIView):
    """
    POST /api/matching/request/
    Body: { nationality, languages, interests, in_team,
            desired_partner, subcategory, role }
    """
    queryset = MatchingRequest.objects.all()
    serializer_class = MatchingRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profile = self.request.user.profile
        nationality = self.request.user.nationality
        serializer.context['nationality'] = nationality
        serializer.context['languages'] = profile.languages

        # ✅ 다시 이걸 써야 함
        serializer.save(user=self.request.user)