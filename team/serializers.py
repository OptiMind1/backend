# team/serializers.py
from rest_framework import serializers
from .models import Team, TeamApplication, CategoryRole, TeamMember

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class TeamApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamApplication
        fields = '__all__'

class CategoryRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRole
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'
