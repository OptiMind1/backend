# merge_dbs.py

import sqlite3

# 1. 로그인용 DB 파일 경로
SRC_DB = 'login_db.sqlite3'

# 2. 메인 애플리케이션 DB 파일 경로
DST_DB = 'db.sqlite3'

def main():
    src = sqlite3.connect(SRC_DB)
    dst = sqlite3.connect(DST_DB)
    sc, dc = src.cursor(), dst.cursor()

    # —————————————————————————————————————
    # 1) 대상 DB에 실제 존재하는 테이블 이름 집합
    dc.execute("""
        SELECT name
          FROM sqlite_master
         WHERE type='table'
           AND name NOT LIKE 'sqlite_%';
    """)
    dst_tables = {row[0] for row in dc.fetchall()}

    # —————————————————————————————————————
    # 2) 원본 DB의 모든 사용자 관련 테이블을 돌며
    sc.execute("""
        SELECT name
          FROM sqlite_master
         WHERE type='table'
           AND name NOT LIKE 'sqlite_%';
    """)
    for (tbl,) in sc.fetchall():
        # 메인 DB에 해당 테이블이 없으면 건너뜀
        if tbl not in dst_tables:
            print(f"→ 스킵: 대상에 테이블 없음 → {tbl}")
            continue

        print(f"→ 복사 중: {tbl}")
        # 컬럼명 리스트
        sc.execute(f"PRAGMA table_info({tbl});")
        cols         = [c[1] for c in sc.fetchall()]
        placeholders = ','.join('?' for _ in cols)
        col_list     = ','.join(cols)

        # 행 단위로 INSERT 시도 (PK 충돌 등은 스킵)
        for row in sc.execute(f"SELECT {col_list} FROM {tbl}"):
            try:
                dc.execute(
                    f"INSERT INTO {tbl} ({col_list}) VALUES ({placeholders})",
                    row
                )
            except sqlite3.IntegrityError as e:
                print(f"    * 스킵된 행 (무결성 오류): {e}")

    # 커밋 및 연결 종료
    dst.commit()
    src.close()
    dst.close()
    print(">> 두 DB 합치기 완료!")

if __name__ == "__main__":
    main()
