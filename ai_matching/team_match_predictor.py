# team_match_predictor.py - 모델 로드 + 점수 예측

import torch
from .team_match_model import TeamMatchMLP
from .team_match_training import create_advanced_feature_vector

import os

def load_trained_model(model_path, input_dim):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, model_path)

    print("📍 모델 파일 위치:", full_path)  # 디버깅용


    model = TeamMatchMLP(input_dim)
    model.load_state_dict(torch.load(full_path, map_location=torch.device("cpu")))
    model.eval()
    return model

def predict_team_score(user, team, model):
    vec = create_advanced_feature_vector(user, team)
    if vec is None:
        return 0.0
    x_tensor = torch.tensor(vec, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        score = model(x_tensor).item()
    return round(score, 4)