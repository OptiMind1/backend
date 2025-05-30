# ai_entry.py - 백엔드 호출용 AI 팀매칭 엔트리포인트

from team_match_predictor import load_trained_model, predict_team_score
from team_match_training import create_advanced_feature_vector, enforce_field_limits
from dl_team_matcher import match_with_preformed_and_individuals

def run_team_matching(input_data):
    """
    input_data 예시:
    {
        "users": [
            { "id": 101, "roles": [...], "interests": [...], "languages": [...], "nationality": ... },
            ...
        ],
        "preformed_teams": [[101, 102], ...],
        "individuals": [103, 104, ...],
        "team_size": 4
    }
    """

    # ✅ 1. 사용자 프로필 딕셔너리 구성 (전처리 포함)
    user_profiles = {
        u["id"]: enforce_field_limits(u)
        for u in input_data["users"]
    }

    # ✅ 2. 모델 로드
    example_user = next(iter(user_profiles.values()))
    vec_dim = len(create_advanced_feature_vector(example_user, [example_user]))
    model = load_trained_model("team_match_advanced.pt", vec_dim)

    # ✅ 3. 팀 매칭 수행
    matched_teams = match_with_preformed_and_individuals(
        preformed_teams=input_data["preformed_teams"],
        individuals=input_data["individuals"],
        profiles=user_profiles,
        model=model,
        team_size=input_data["team_size"]
    )

    # ✅ 4. 결과 포맷 변환
    result = []
    for i, team in enumerate(matched_teams):

        result.append({
            "team_id": f"T{i+1}",
            "members": [
                {
                    "user_id": uid,
                    "role": user_profiles[uid]["roles"],
                    "nationality": user_profiles[uid]["nationality"],
                    "interests": user_profiles[uid]["interests"]
                } for uid in team
            ]
        })

    return result
