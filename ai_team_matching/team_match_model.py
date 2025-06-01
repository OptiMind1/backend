# team_match_model.py - 딥러닝 기반 팀 적합도 예측 모델 정의

import torch
import torch.nn as nn

class TeamMatchMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim=128):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()  # 출력: 0~1 사이의 점수
        )

    def forward(self, x):
        return self.mlp(x).squeeze()
