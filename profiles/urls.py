from django.urls import path
from .views import (
    ProfileCreateView,
    ProfileMeView,
    ProfileUpdateView,
    ProfileSearchView)

urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name='profile-create'),
    path('me/', ProfileMeView.as_view(), name='profile-me'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update'), 
    path('search/', ProfileSearchView.as_view(), name='profile-search'),

]
