# competition/utils.py

from .models import CompetitionCategory

# 1) 소분류(subcategory) 맵핑
SUBCATEGORY_KEYWORDS = {
    # 대분류 IDEA
    "아이디어·창업·네이밍": ["창업", "아이디어", "슬로건", "네이밍", "마케팅"],
    # 대분류 MEDIA
    "사진·영상": ["사진", "영상"],
    # 대분류 DESIGN
    "디자인·그림·웹툰": ["포스터", "로고", "상품", "캐릭터", "그림", "웹툰", "광고", "도시건"],
    # 대분류 LITERATURE
    "문학·학술·공학": ["논문", "수기", "시 ", "시나리오", "공학", "과학"],
    # 대분류 ARTS
    "예체능·e스포츠": ["음악", "댄스", "e스포츠"],
}

def classify_subcategory(title: str) -> str:
    """
    제목에 포함된 키워드를 바탕으로 소분류(subcategory)를 반환.
    매핑된 키워드 중 가장 먼저 매치된 항목을 리턴.
    """
    t = title.lower()
    for big_cat, keywords in SUBCATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in t:
                return kw  # 예: "창업", "슬로건", "사진", "포스터" 등
    return "기타"

def classify_category(title: str) -> str:
    """
    classify_subcategory로 먼저 subcategory를 뽑고,
    그 subcategory가 속한 대분류(TextChoices)를 반환.
    """
    sub = classify_subcategory(title)
    # 소분류 키워드를 돌며 어느 대분류 소속인지 확인
    for big_cat, keywords in SUBCATEGORY_KEYWORDS.items():
        if sub in [kw for kw in keywords]:
            # TextChoices 값으로 반환
            return getattr(CompetitionCategory, big_cat.replace("·", "_"), CompetitionCategory.ETC)
    return CompetitionCategory.ETC
