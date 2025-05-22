from django.core.management.base import BaseCommand
from competition.models import Competition
from team.models import Team

class Command(BaseCommand):
    help = '모든 Competition마다 Team 객체를 하나씩 생성합니다.'

    def handle(self, *args, **options):
        created = 0
        for comp in Competition.objects.all():
            # 이미 팀이 있으면 건너뛰기
            if Team.objects.filter(competition=comp).exists():
                continue
            Team.objects.create(competition=comp)
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ 생성 완료: {created}개의 Team을 만들었습니다.'
        ))
