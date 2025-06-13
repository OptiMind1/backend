from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
from .utils import classify_subcategory, classify_category
from .models import Competition


def fetch_allcon_competitions_selenium():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--lang=ko_KR")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    contests = []
    MAX_PAGES = 6  # 페이지 수 조절 가능 (15개 x 4 = 약 60개)

    for page in range(1, MAX_PAGES + 1):
        print(f"📄 페이지 {page} 크롤링 중...")
        url = f"https://www.all-con.co.kr/list/contest/1/{page}?sortname=cl_order&sortorder=asc"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tbl-list tr"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.select("#tbl-list tr")

        print("🔍 현재 페이지 항목 수:", len(items))

        for item in items:
            title_tag = item.select_one("td.title a")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = title_tag["href"]
            if not link.startswith("http"):
                link = "https://www.all-con.co.kr" + link

            # 상세 페이지 진입
            driver.get(link)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.contest_poster img"))
                )
            except:
                print("❌ 이미지 로딩 실패 (타임아웃)")

            detail_soup = BeautifulSoup(driver.page_source, "html.parser")

            # 이미지 추출
            image_tag = detail_soup.select_one("div.contest_poster img")
            image_url = ""
            if image_tag and image_tag.has_attr("src"):
                image_url = image_tag["src"]
                if image_url.startswith("/"):
                    image_url = "https://www.all-con.co.kr" + image_url

            print(f"📸 이미지: {image_url}")

            # 본문 HTML 추출
            desc_container = (
                detail_soup.select_one("div.board_body_txt#contest_body")
                or detail_soup.select_one("div.board_body_txt")
                or detail_soup.select_one("div.view_contest")
                or detail_soup.select_one("#contents")
            )
            description_html = desc_container.decode_contents() if desc_container else ""

            contests.append({
                "title": title,
                "category": classify_category(title),
                "subcategory": classify_subcategory(title),
                "description": description_html,
                "link": link,
                "image_url": image_url,
            })

            print(f"✅ 누적 {len(contests)}개: {title}")

            time.sleep(0.5)  # 너무 빠른 요청 방지

    driver.quit()
    return contests


def save_allcon_to_db():
    entries = fetch_allcon_competitions_selenium()
    saved = 0

    for entry in entries:
        try:
            if not Competition.objects.filter(title=entry["title"]).exists():
                Competition.objects.create(
                    title=entry["title"],
                    category=entry["category"],
                    subcategory=entry["subcategory"],
                    description=entry["description"],
                    link=entry["link"],
                    image_url=entry["image_url"],
                    host="",
                    deadline=None,
                )
                saved += 1
        except Exception as e:
            print(f"❌ 저장 실패: {entry['title']} - {e}")
            print("🔎 entry:", entry)

    print(f"🎉 총 {saved}개 공모전 저장됨")
    return saved


def fetch_competition_detail_page(detail_url):
    from bs4 import BeautifulSoup
    import requests

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    if not detail_url.startswith("http"):
        detail_url = "https://www.all-con.co.kr" + detail_url

    try:
        resp = requests.get(detail_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        image_url = ""
        image_tag = soup.select_one(".view_thumb img, img.poster-img")
        if image_tag and image_tag.has_attr("src"):
            image_url = image_tag["src"]
            if image_url.startswith("/"):
                image_url = "https://www.all-con.co.kr" + image_url

        desc_container = (
            soup.select_one("div.board_body_txt#contest_body")
            or soup.select_one("div.board_body_txt")
            or soup.select_one("div.view_contest")
            or soup.select_one("#contents")
        )
        description = desc_container.decode_contents() if desc_container else ""

        return {
            "image_url": image_url,
            "description": description,
        }

    except Exception as e:
        print(f"❌ 상세 페이지 크롤링 실패: {detail_url} - {e}")
        return {
            "image_url": "",
            "description": "",
        }
