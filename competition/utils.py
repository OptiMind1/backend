# competition/utils.py

from .models import CompetitionCategory

# 소분류 ↔ 대분류 맵
SUBCATEGORY_KEYWORDS = {
    "아이디어·창업·네이밍": ["창업", "아이디어", "슬로건", "네이밍", "마케팅"],
    "사진·영상":           ["사진", "영상"],
    "디자인·그림·웹툰":     ["포스터", "로고", "상품", "캐릭터", "그림", "웹툰", "광고", "도시건축"],
    "문학·학술·공학":       ["논문", "수기", "시", "시나리오", "공학", "과학"],
    "예체능·e스포츠":       ["음악", "댄스", "e스포츠"],
}

def classify_subcategory(title: str) -> str:
    t = title.lower()
    for big_cat, kws in SUBCATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return kw
    return "기타"

def classify_category(title: str) -> str:
    """
    subcategory를 뽑아 온 다음,
    그 subcategory가 속한 대분류 값을 CompetitionCategory enum의 value 로 반환.
    """
    sub = classify_subcategory(title)
    for big_cat, kws in SUBCATEGORY_KEYWORDS.items():
        if sub in kws:
            # CompetitionCategory(big_cat) → enum 멤버(IDEA, MEDIA…) 반환
            try:
                return CompetitionCategory(big_cat).value
            except ValueError:
                pass
    return CompetitionCategory.ETC.value