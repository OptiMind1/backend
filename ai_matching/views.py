# views.py (백엔드 API 예시)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# AI 함수 가져오기
from ai_entry import run_team_matching

@csrf_exempt
def team_matching_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = run_team_matching(data)
            return JsonResponse({"teams": result}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST only"}, status=405)
