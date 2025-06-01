from itertools import combinations, permutations
from team_match_predictor import predict_team_score
from team_match_training import create_advanced_feature_vector

# 팀 크기 분할: team_size 또는 team_size - 1만 허용
def get_team_sizes_fixed_max(team_size, total_users):
    max_teams = total_users // (team_size - 1)
    while max_teams > 0:
        small_size = team_size - 1
        num_full = total_users - (max_teams * small_size)
        if 0 <= num_full <= max_teams:
            return [team_size] * num_full + [small_size] * (max_teams - num_full)
        max_teams -= 1
    raise ValueError("⚠️ 인원을 해당 팀 크기로 나눌 수 없습니다.")

# 개인 지원자 팀 구성: 최적 조합 선택
def match_individuals_by_score(individuals, profiles, model, team_size):
    team_sizes = get_team_sizes_fixed_max(team_size, len(individuals))
    team_candidates = []

    for size in set(team_sizes):
        for team in combinations(individuals, size):
            others = [profiles[u] for u in team]
            score = sum(predict_team_score(profiles[u], [p for i, p in enumerate(others) if team[i] != u], model) for u in team)
            avg_score = score / len(team)
            team_candidates.append((team, avg_score))

    team_candidates.sort(key=lambda x: x[1], reverse=True)

    # 중복 없이 최적 팀 조합 선택
    best_combination = []
    used = set()
    for team, score in team_candidates:
        if any(u in used for u in team):
            continue
        best_combination.append(list(team))
        used.update(team)
        if len(best_combination) == len(team_sizes):
            break
    return best_combination

# 전체 팀 매칭 함수
def match_with_preformed_and_individuals(preformed_teams, individuals, profiles, model, team_size=4):
    matched_teams = []
    used_individuals = set()

    # ✅ 1. 사전 구성 팀 보완
    for team in preformed_teams:
        needed = team_size - len(team)
        if needed <= 0:
            matched_teams.append(team)
            continue
        partial_profiles = [profiles[u] for u in team]
        candidates = [u for u in individuals if u not in used_individuals]
        scored = [
            (uid, predict_team_score(profiles[uid], partial_profiles, model))
            for uid in candidates
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        added = [uid for uid, _ in scored[:needed]]
        matched_teams.append(team + added)
        used_individuals.update(added)

    # ✅ 2. 개인 지원자 최적 조합
    remaining = [u for u in individuals if u not in used_individuals]
    new_teams = match_individuals_by_score(remaining, profiles, model, team_size)
    matched_teams.extend(new_teams)

    return matched_teams
