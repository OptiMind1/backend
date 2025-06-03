import requests
from bs4 import BeautifulSoup
from .utils import classify_subcategory, classify_category


def fetch_allcon_competitions():
    """
    Allcon(https://www.all-con.co.kr)의 대학생·일반인 공모전 목록을 크롤링해서
    Competition 모델에 맞춰 dict 리스트로 반환합니다.
    """
    url = "https://www.all-con.co.kr/list.php?ac_group=1"
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

    for item in soup.select("ul.list-con > li.list-row"):
        title_tag = item.select_one("strong.tit")
        category_tag = item.select_one("span.cate")
        date_tag = item.select_one("span.date")
        link_tag = item.select_one("a")

        if not (title_tag and category_tag and date_tag and link_tag):
            continue

        title_text = title_tag.get_text(strip=True)
        entry_sub = classify_subcategory(title_text)
        entry_cat = classify_category(title_text)

        link = link_tag["href"] if link_tag.has_attr("href") else ""
        detail_info = fetch_competition_detail_page(link)

        contests.append({
            "title": title_text,
            "subcategory": entry_sub,
            "category": entry_cat,
            "deadline": None,
            "link": link,
            # React 쪽에서 HTML 전체를 렌더링할 수 있도록 description 필드에 HTML을 담습니다.
            "description": detail_info.get("description", ""),
            "image_url": detail_info.get("image_url", ""),
        })

    return contests


def fetch_competition_detail_page(detail_url):
    """
    Allcon 상세 페이지(예: /view/contest/520261)에서
    1) contest_field 테이블(주최/주관/접수기간/분야/응모대상/혜택)을 재조립하여 HTML로 가져오고,
    2) 본문(유튜브 포함: 모집개요, 기간 및 일정, 접수방법, 혜택내역, 문의 등) 전체를
       decode_contents()로 “HTML 그대로” 가져와서 합친 뒤 반환합니다.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/113.0.0.0 Safari/537.36"
            )
        }

        # 1) detail_url을 절대 URL로 변환
        if detail_url.startswith("http"):
            full_url = detail_url
        else:
            full_url = "https://www.all-con.co.kr" + detail_url

        resp = requests.get(full_url, headers=headers, timeout=10)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        # ─────────────── 2) 포스터 이미지 추출 ───────────────
        image_url = ""
        thumb = soup.select_one(".view_thumb img")
        if thumb and thumb.has_attr("src"):
            image_url = thumb["src"]
        else:
            poster_img = soup.select_one("img.poster-img")
            if poster_img and poster_img.has_attr("src"):
                image_url = poster_img["src"]
            else:
                any_poster = soup.find("img", src=lambda s: s and "poster" in s)
                if any_poster and any_poster.has_attr("src"):
                    image_url = any_poster["src"]

        if image_url.startswith("/"):
            image_url = "https://www.all-con.co.kr" + image_url

        # ─────────────── 3) contest_field 테이블 재조립 ───────────────
        clean_table_html = ""
        contest_field = soup.select_one("div.contest_field")
        if contest_field:
            tbl_tag = contest_field.find("table")
            if tbl_tag:
                rows = []
                for tr in tbl_tag.select("tbody tr"):
                    th = tr.select_one("th")
                    td = tr.select_one("td")
                    if th and td:
                        th_html = str(th)
                        td_html = str(td)
                        rows.append(f"<tr>{th_html}{td_html}</tr>")

                if rows:
                    caption_tag = tbl_tag.find("caption")
                    caption_html = str(caption_tag) if caption_tag else ""
                    new_table = (
                        f"<table>"
                        f"{caption_html}"
                        f"<tbody>{''.join(rows)}</tbody>"
                        f"</table>"
                    )
                    clean_table_html = f"<div class='detail-table'>{new_table}</div>"

        # ─────────────── 4) 본문(유튜브 + 모집개요~문의) 전체 HTML 가져오기 ───────────────
        desc_html = ""
        # 올-콘 사이트 실제 HTML을 살펴보니, 본문(유튜브 포함)은 대개 다음 블록 중 하나에 들어있습니다.
        desc_container = (
            soup.select_one("div.board_body_txt#contest_body")
            or soup.select_one("div.board_body_txt")
            or soup.select_one("div.board_body")
            or soup.select_one("div.contBox")
            or soup.select_one("div.view_contest")
            or soup.select_one("#contents")
            or soup.select_one("div.view_cont")
            or soup.select_one("section.contBox")
            or soup.select_one("div.tb_cont")
            or soup.select_one(".infoCont")
            or soup.select_one("article")
            or None
        )

        if desc_container:
            # decode_contents(): 내부의 모든 HTML(유튜브 태그, <p>, <font>, &nbsp; 포함)을 통째로 가져옵니다.
            desc_html = desc_container.decode_contents()
        else:
            # 최후의 수단: view_info 안의 <li> 항목 HTML을 가져오기
            info_div = soup.select_one("div.view_info")
            if info_div:
                desc_html = info_div.decode_contents()

        # ─────────────── 5) 테이블 + 본문 전체 HTML 합치기 ───────────────
        full_html = ""
        if clean_table_html:
            full_html += clean_table_html + "<hr />"
        if desc_html:
            full_html += f"<div class='detail-body'>{desc_html}</div>"

        return {
            "image_url": image_url or "",
            "description": full_html or "",
        }

    except Exception as e:
        # 치명적 에러가 난 경우 빈값으로 리턴합니다.
        print(f"[ERROR] 상세 페이지 크롤링 실패: {e}")
        return {
            "image_url": "",
            "description": "",
        }
