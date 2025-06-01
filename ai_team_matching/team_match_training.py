# team_match_training.py - 팀 적합도 예측 모델 학습 + 입력 필터링 + 벡터 생성
import os  
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from .team_match_model import TeamMatchMLP

# 역할/관심사/언어/국적 리스트
ALL_ROLES = [
    "기획", "디자이너", "UX/UI 설계자", "촬영/감독", "영상 편집자", "사진 후보정자",
    "발표자/피칭", "분석/리서처", "자료 조사", "데이터 수집/분석", "문서화 담당자",
    "브랜딩/마케팅", "통역/언어", "프론트엔드 개발자", "백엔드 개발자", "AI/데이터 개발자",
    "음향/음악 담당자", "게이머/플레이어", "연출/무대기획자"
]

ALL_INTERESTS = [
    "창업", "아이디어", "슬로건", "네이밍", "마케팅",
    "사진", "영상", "포스터", "로고", "상품",
    "캐릭터", "그림", "웹툰", "광고", "도시건축",
    "논문", "수기", "시", "시나리오", "공학",
    "과학", "음악", "댄스", "e스포츠", "기타"
]

ALL_LANGUAGES = ["Korean", "English", "Vietnamese", "Hindi", "Chinese", "Japanese", "French", "German", "Spanish", "Arabic"]
ALL_NATIONALITIES = ["Korea", "USA", "Vietnam", "India", "China", "Japan", "France", "Germany", "Mexico", "Brazil", "UK", "Canada", "Indonesia", "Russia", "Spain"]

# ✅ 필드 개수 제한 + 결측값 대체
def enforce_field_limits(user, max_items=3):
    def limit(field, allow_empty=False):
        values = user.get(field, [])
        values = values[:max_items]
        if not values and not allow_empty:
            values = ["없음"]
        return values
    return {
        "roles": limit("roles"),
        "interests": limit("interests"),
        "languages": limit("languages"),
        "nationality": user.get("nationality", "Unknown")
    }

# ✅ 벡터화 + 정규화
def create_advanced_feature_vector(user, team):
    def encode(values, vocab):
        return [1 if v in values else 0 for v in vocab]

    user_vec = (
        encode(user.get("roles", []), ALL_ROLES) +
        encode(user.get("interests", []), ALL_INTERESTS) +
        encode(user.get("languages", []), ALL_LANGUAGES) +
        [1 if user.get("nationality") == n else 0 for n in ALL_NATIONALITIES]
    )

    team_roles = sum([m.get("roles", []) for m in team], [])
    team_interests = sum([m.get("interests", []) for m in team], [])
    team_langs = sum([m.get("languages", []) for m in team], [])
    team_nats = [m.get("nationality") for m in team]

    team_vec = (
        encode(team_roles, ALL_ROLES) +
        encode(team_interests, ALL_INTERESTS) +
        encode(team_langs, ALL_LANGUAGES) +
        [team_nats.count(n) for n in ALL_NATIONALITIES]
    )

    role_overlap = len(set(user.get("roles", [])) & set(team_roles))
    interest_union = set(user.get("interests", [])).union(set(team_interests))
    interest_inter = set(user.get("interests", [])).intersection(set(team_interests))
    inter_jaccard = len(interest_inter) / len(interest_union) if interest_union else 0
    nat_diversity = len(set(team_nats))
    lang_overlap = len(set(user.get("languages", [])) & set(team_langs))

    vec = user_vec + team_vec + [role_overlap, inter_jaccard, nat_diversity, lang_overlap]
    
    if np.count_nonzero(vec) < 2:
        return None
    norm = np.linalg.norm(vec)
    return (np.array(vec) / norm).tolist() if norm > 0 else None

# ✅ 학습용 더미 샘플 생성
def create_advanced_dummy_samples(num_samples=1000):
    samples = []
    for _ in range(num_samples):
        user = enforce_field_limits({
            "roles": random.sample(ALL_ROLES, random.randint(0, 4)),
            "interests": random.sample(ALL_INTERESTS, random.randint(0, 4)),
            "languages": random.sample(ALL_LANGUAGES, random.randint(0, 4)),
            "nationality": random.choice(ALL_NATIONALITIES)
        })
        team = [enforce_field_limits({
            "roles": random.sample(ALL_ROLES, random.randint(0, 4)),
            "interests": random.sample(ALL_INTERESTS, random.randint(0, 4)),
            "languages": random.sample(ALL_LANGUAGES, random.randint(0, 4)),
            "nationality": random.choice(ALL_NATIONALITIES)
        }) for _ in range(random.randint(2, 4))]

        label = random.uniform(0.4, 0.9)
        vec = create_advanced_feature_vector(user, team)
        if vec:
            samples.append((vec, label))
    return samples

# ✅ 모델 학습 및 저장 (경로 포함 버전)
def train_model(samples, input_dim, save_name="team_match_advanced.pt"):
    class SampleDataset(Dataset):
        def __init__(self, data):
            self.data = data
        def __len__(self):
            return len(self.data)
        def __getitem__(self, idx):
            x, y = self.data[idx]
            return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

    model = TeamMatchMLP(input_dim)
    loader = DataLoader(SampleDataset(samples), batch_size=64, shuffle=True)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    for epoch in range(5):
        total_loss = 0
        for x, y in loader:
            optimizer.zero_grad()
            pred = model(x)
            loss = loss_fn(pred, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"[Epoch {epoch+1}] Loss: {total_loss / len(loader):.4f}")

    # 🔹 현재 파일 기준 경로로 저장
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(base_dir, save_name)

    torch.save(model.state_dict(), save_path)
    print(f"✅ 모델 저장 완료 → {save_path}")

if __name__ == "__main__":
    samples = create_advanced_dummy_samples(1000)
    print(f"📊 유효 샘플 수: {len(samples)}")  # <- 이거 반드시 확인

    if not samples:
        print("❌ 유효한 학습 샘플이 없습니다. 학습 중단.")
    else:
        input_dim = len(samples[0][0])
        train_model(samples, input_dim)
