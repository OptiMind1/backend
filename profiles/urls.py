from django.urls import path
from .views import (
    ProfileCreateView,
    ProfileMeView,
    ProfileUpdateView,
    ProfileSearchView,
    CheckNicknameView,
    TeamMemberSearchView)

urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name='profile-create'),
    path('me/', ProfileMeView.as_view(), name='profile-me'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update'), 
    path('search/', ProfileSearchView.as_view(), name='profile-search'),
    path('check_nickname/', CheckNicknameView.as_view(), name='check-nickname'),
    path('search_team/', TeamMemberSearchView.as_view(), name='search-team-members'),

]
