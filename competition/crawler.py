import requests
from bs4 import BeautifulSoup
from .utils import classify_subcategory, classify_category

def fetch_competition_detail_page(detail_url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }

        full_url = detail_url if detail_url.startswith("http") else "https://www.all-con.co.kr" + detail_url
        resp = requests.get(full_url, headers=headers, timeout=10)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        # 이미지 URL 추출
        image_url = ""
        thumb = soup.select_one(".view_thumb img") or soup.select_one("img.poster-img") or soup.find("img", src=lambda s: s and "poster" in s)
        if thumb and thumb.has_attr("src"):
            image_url = thumb["src"]

        if image_url.startswith("/"):
            image_url = "https://www.all-con.co.kr" + image_url

        # 본문 설명 추출
        desc_html = ""
        container = (
            soup.select_one(".board_body_txt")
            or soup.select_one("div.view_cont")
            or soup.select_one("div.board_body")
            or soup.select_one("section.contBox")
        )
        if container:
            desc_html = container.decode_contents()

        return {
            "image_url": image_url,
            "description": desc_html
        }

    except Exception as e:
        print(f"[ERROR] 상세페이지 크롤링 실패: {e}")
        return {"image_url": "", "description": ""}

def fetch_allcon_competitions():
    """
    Allcon 공모전 목록을 크롤링해서 DB 저장용 데이터 리스트 반환
    """
    url = "https://www.all-con.co.kr/list/?c=1"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    contests = []
    contest_items = soup.select("ul.list li")

    print(f"🔎 공모전 항목 수: {len(contest_items)}")

    for item in contest_items:
        title_tag = item.select_one("strong.tit")
        link_tag = item.select_one("a")

        if not title_tag or not link_tag:
            continue

        title_text = title_tag.get_text(strip=True)
        link = link_tag.get("href", "")

        entry_sub = classify_subcategory(title_text)
        entry_cat = classify_category(title_text)

        detail_info = fetch_competition_detail_page(link)

        contests.append({
            "title": title_text,
            "subcategory": entry_sub,
            "category": entry_cat,
            "deadline": None,
            "link": link,
            "description": detail_info.get("description", ""),
            "image_url": detail_info.get("image_url", ""),
        })

    print(f"✅ 최종 크롤링된 개수: {len(contests)}")
    return contests
