# ai_matching/urls.py
from django.urls import path
from .views import team_matching_api

urlpatterns = [
    path('ai-matching/', team_matching_api, name='ai-matching'),
]