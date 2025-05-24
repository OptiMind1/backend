from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from competition.models import Competition, CompetitionCategory
from datetime import datetime
import time

CATEGORY_SOURCES = [
    ("대학생 공모전", "https://www.all-con.co.kr/list/contest/1?page={}"),
    ("대학생 대외활동", "https://www.all-con.co.kr/list/contest/2?page={}"),
]

PAGE_RANGE = range(1, 35)  # 1~34 페이지


# 카테고리 분류 함수
def classify_category(title: str) -> CompetitionCategory:
    title = title.lower()
    if any(word in title for word in ["영상", "미디어", "사진", "콘텐츠"]):
        return CompetitionCategory.MEDIA
    elif any(word in title for word in ["소프트웨어", "앱", "코딩", "ai", "인공지능", "데이터", "개발"]):
        return CompetitionCategory.SOFTWARE
    elif any(word in title for word in ["창업", "마케팅", "경영", "스타트업", "브랜드", "경제"]):
        return CompetitionCategory.BUSINESS
    elif any(word in title for word in ["과학", "공학", "기술", "실험", "자연", "생명"]):
        return CompetitionCategory.SCIENCE
    elif any(word in title for word in ["교육", "인권", "복지", "사회", "청소년", "아동"]):
        return CompetitionCategory.EDUCATION
    elif any(word in title for word in ["건축", "도시", "환경", "지속가능", "기후"]):
        return CompetitionCategory.ENVIRONMENT
    elif any(word in title for word in ["디자인", "예술", "그림", "일러스트", "웹툰", "로고", "포스터"]):
        return CompetitionCategory.ART
    elif any(word in title for word in ["아이디어", "기획", "슬로건", "네이밍"]):
        return CompetitionCategory.IDEA
    return CompetitionCategory.ETC


class Command(BaseCommand):
    help = 'Selenium으로 Allcon 대학생 공모전/대외활동 다중 페이지 크롤링'

    def handle(self, *args, **kwargs):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        for label, base_url in CATEGORY_SOURCES:
            self.stdout.write(self.style.SUCCESS(f"\n🚀 크롤링 시작: {label}"))
            for page_num in PAGE_RANGE:
                url = base_url.format(page_num)
                driver.get(url)
                time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                rows = soup.select('#tbl-list tr')

                if not rows:
                    self.stdout.write(self.style.WARNING(f"⚠️ 페이지 {page_num}: 항목 없음"))
                    continue

                for row in rows:
                    try:
                        tds = row.find_all('td')
                        if len(tds) < 4:
                            continue

                        title = tds[0].get_text(strip=True)
                        host = tds[1].get_text(strip=True)
                        date_text = tds[2].get_text(strip=True)
                        link_tag = tds[0].find('a')
                        link = 'https://www.all-con.co.kr' + link_tag['href'] if link_tag else 'https://www.all-con.co.kr'

                        # 날짜 파싱
                        try:
                            deadline_str = date_text.split('~')[-1].strip()
                            deadline = datetime.strptime(deadline_str, '%y.%m.%d').date()
                        except:
                            deadline = None

                        if Competition.objects.filter(title=title).exists():
                            self.stdout.write(f"⚠️ 중복: {title}")
                            continue

                        category = classify_category(title)

                        Competition.objects.create(
                            title=title,
                            host=host,
                            deadline=deadline,
                            link=link,
                            category=category,
                            description="Allcon에서 수집된 공모전입니다."
                        )
                        self.stdout.write(self.style.SUCCESS(f"✅ 등록 완료: {title}"))

                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"❌ 오류 발생: {e}"))

        driver.quit()
        self.stdout.write(self.style.SUCCESS("🎉 모든 공모전 크롤링 완료!"))
