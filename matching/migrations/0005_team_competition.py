# Generated by Django 5.2.1 on 2025-06-03 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0010_alter_competition_subcategory'),
        ('matching', '0004_team_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='competition',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='competition.competition'),
            preserve_default=False,
        ),
    ]
