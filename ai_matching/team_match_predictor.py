# team_match_predictor.py - 모델 로드 + 점수 예측

import torch
from team_match_model import TeamMatchMLP
from team_match_training import create_advanced_feature_vector

def load_trained_model(model_path, input_dim):
    model = TeamMatchMLP(input_dim)
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
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
