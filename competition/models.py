# competition/models.py

from django.db import models

class CompetitionCategory(models.TextChoices):
    IDEA       = ('아이디어·창업·네이밍', '아이디어·창업·네이밍')
    MEDIA      = ('사진·영상',           '사진·영상')
    DESIGN     = ('디자인·그림·웹툰',     '디자인·그림·웹툰')
    LITERATURE = ('문학·학술·공학',       '문학·학술·공학')
    ARTS       = ('예체능·e스포츠',       '예체능·e스포츠')
    ETC        = ('기타',               '기타')

class CompetitionSubcategory(models.TextChoices):
    # IDEA 서브항목
    STARTUP      = ('창업',     '창업')
    IDEA         = ('아이디어', '아이디어')
    SLOGAN       = ('슬로건',   '슬로건')
    NAMING       = ('네이밍',   '네이밍')
    MARKETING    = ('마케팅',   '마케팅')

    # MEDIA 서브항목
    PHOTO        = ('사진',     '사진')
    VIDEO        = ('영상',     '영상')

    # DESIGN 서브항목
    POSTER       = ('포스터',    '포스터')
    LOGO         = ('로고',      '로고')
    PRODUCT      = ('상품',      '상품')
    CHARACTER    = ('캐릭터',    '캐릭터')
    ILLUSTRATION = ('그림',      '그림')
    WEBTOON      = ('웹툰',      '웹툰')
    AD           = ('광고',      '광고')
    URBAN        = ('도시건축',    '도시건축')

    # LITERATURE 서브항목
    PAPER        = ('논문',      '논문')
    ESSAY        = ('수기',      '수기')
    POETRY       = ('시',        '시')
    SCREENPLAY   = ('시나리오',  '시나리오')
    ENGINEERING  = ('공학',      '공학')
    SCIENCE      = ('과학',      '과학')

    # ARTS 서브항목
    MUSIC        = ('음악',      '음악')
    DANCE        = ('댄스',      '댄스')
    ESPORTS      = ('e스포츠',   'e스포츠')

    # 기타
    OTHER        = ('기타',      '기타')

class Competition(models.Model):
    title       = models.CharField(max_length=200)
    category    = models.CharField(
        max_length=20,
        choices=CompetitionCategory.choices,
        default=CompetitionCategory.ETC
    )
    subcategory = models.CharField(
        max_length=50,
        choices=CompetitionSubcategory.choices,      # ← 세부항목 choices 지정
        default=CompetitionSubcategory.OTHER,
        help_text="세부항목 분류 (e.g. 창업, 영상, 포스터 등)"
    )
    host        = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    deadline    = models.DateField(null=True, blank=True)
    link        = models.URLField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
