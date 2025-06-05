# ai_entry.py - 백엔드 호출용 AI 팀매칭 엔트리포인트

from .team_match_predictor import load_trained_model, predict_team_score
from .team_match_training import create_advanced_feature_vector, enforce_field_limits
from .dl_team_matcher import match_with_preformed_and_individuals

def run_team_matching(input_data):
    """
    input_data 예시:
    {
        "users": [
            { "id": ..., "interests": [...], "languages": [...], "nationality": ... },
            ...
        ],
        "preformed_teams": [
            {
                "members": [
                    { "id": ..., "roles": [...] },
                    ...
                ]
            },
            ...
        ],
        "individuals": [
            { "id": ..., "roles": [...] },
            ...
        ],
        "team_size": 4
    }
    """

    # 1. 사용자 공통 프로필 (roles 제외)
    user_info_map = {
        u["id"]: enforce_field_limits(u, skip_roles=True)
        for u in input_data["users"]
    }

    # 2. 역할 포함된 user_profiles 구성
    def add_roles(user_id, roles):
        base = user_info_map.get(user_id, {})
        base["roles"] = roles if roles else ["없음"]
        return base

    user_profiles = {}

    # 팀 지원자 처리
    for team in input_data.get("preformed_teams", []):
        for member in team["members"]:
            user_profiles[member["id"]] = add_roles(member["id"], member.get("roles", []))

    # 개인 지원자 처리
    for user in input_data.get("individuals", []):
        user_profiles[user["id"]] = add_roles(user["id"], user.get("roles", []))

    # 3. 모델 로드
    example_user = next(iter(user_profiles.values()))
    vec_dim = len(create_advanced_feature_vector(example_user, [example_user]))
    model = load_trained_model("team_match_advanced.pt", vec_dim)

    # 4. 팀 매칭 수행
    matched_teams = match_with_preformed_and_individuals(
        preformed_teams=[
            [member["id"] for member in team["members"]]
            for team in input_data.get("preformed_teams", [])
        ],
        individuals=[u["id"] for u in input_data.get("individuals", [])],
        profiles=user_profiles,
        model=model,
        team_size=input_data["team_size"]
    )

    # 5. 결과 포맷
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
