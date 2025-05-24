# competition/crawler.py

import requests
from bs4 import BeautifulSoup
from .utils import classify_subcategory, classify_category

def fetch_allcon_competitions():
    """
    Allcon(https://www.all-con.co.kr)의 대학생·일반인 공모전 목록을 크롤링해서
    Competition 모델에 맞춰 dict 리스트로 반환합니다.
    """
    # 올콘 예전 공모전 목록 URL (ac_group=1)
    url = "https://www.all-con.co.kr/list.php?ac_group=1"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    contests = []
    # 페이지 구조에 맞춘 셀렉터:
    #  - <ul class="list-con"> 안에 <li class="list-row"> 항목이 있는 구조
    for item in soup.select("ul.list-con > li.list-row"):
        title_tag    = item.select_one("strong.tit")
        category_tag = item.select_one("span.cate")
        date_tag     = item.select_one("span.date")
        link_tag     = item.select_one("a")

        if not (title_tag and category_tag and date_tag):
            continue

        title_text = title_tag.get_text(strip=True)

        # 소분류(subcategory)와 대분류(category) 분류
        entry_sub = classify_subcategory(title_text)
        entry_cat = classify_category(title_text)

        contests.append({
            "title":       title_text,
            "subcategory": entry_sub,
            "category":    entry_cat,
            "deadline":    None,  # 마감일 정보가 따로 없으면 None
            "link":        link_tag["href"] if link_tag and link_tag.has_attr("href") else "",
            "description": ""     # 필요 시 description 크롤링 로직 추가
        })

    return contests
