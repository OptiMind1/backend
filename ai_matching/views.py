# views.py (백엔드 API 예시)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# AI 함수 가져오기
from ai_matching.ai_entry import run_team_matching

# 추가한 거
from team.models import Team
from matching.models import MatchingRequest
from users.models import User
from profiles.models import Profile
import uuid  # 팀 고유 ID 생성용
from competition.models import Competition  


@csrf_exempt
def team_matching_api(request):
    if request.method == 'POST':
        try:
            # data = json.loads(request.body) # 기존

            # 수정 후
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
            else:
                return JsonResponse({"error": "Invalid content type"}, status=400)


            result = run_team_matching(data) # AI 매칭 결과 리스트

            # 🔥 competition 객체 먼저 가져오기
            comp_id = data.get("competition")
            if not comp_id:
                return JsonResponse({"error": "competition ID가 누락됨"}, status=400)

            competition = Competition.objects.get(id=comp_id)  # ← 여기 추가

            for team_info in result:
                team_obj = Team.objects.create(
                    name=team_info["team_id"],
                    competition=competition
                )

                for member in team_info["members"]:
                    user_id = member["user_id"]
                    role = member["role"]
                    user = User.objects.get(user_id=user_id)
                    profile = Profile.objects.get(user=user)

                    MatchingRequest.objects.create(
                        user=user,
                        # profile=profile,
                        team=team_obj,
                        in_team=True,
                        desired_partner="",
                        # role=", ".join(role)
                        role=role,


                        nationality=member.get("nationality", "Unknown"),
                        languages=member.get("languages", []),
                        interests=member.get("interests", []),
                        competition=competition,  # 이 값을 프론트에서 넘기게 해야 함
                        team_group_id=None  # AI 매칭 후 생성된 팀은 팀 신청 그룹과 무관함
                    )

            return JsonResponse({"teams": result}, status=200)
        except Exception as e:
            import traceback
            print("🔥 예외 발생:", e)
            traceback.print_exc()  # ← 이거 꼭 추가!
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST only"}, status=405)