# app/app.py
import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="서울 출퇴근 EDA", layout="wide")
st.title("공개데이터 EDA 대시보드 (서울 출퇴근)")

st.write("CSV/XLSX 업로드 → 기본 통계/차트  ·  그리고 **DB에서 AM/PM 평균속도 지표**를 불러옵니다.")

# =========================
# 1) 파일 업로드 EDA 섹션
# =========================
st.header("① 파일 업로드(로컬 데이터 미리보기)")

file = st.file_uploader("CSV 또는 XLSX 업로드", type=["csv", "xlsx"])
force_cp949 = st.checkbox("강제 CP949로 읽기(윈도우 CSV 오류 시)")

df = None
if file:
    name = file.name.lower()
    try:
        if name.endswith(".xlsx"):
            # XLSX는 인코딩 이슈 없음 (openpyxl 필요)
            df = pd.read_excel(file)
            st.caption("형식: XLSX (인코딩 문제 없음)")
        else:
            if force_cp949:
                file.seek(0)
                df = pd.read_csv(file, encoding="cp949", errors="ignore")
                st.caption("강제 인코딩: cp949 (일부 문자를 무시할 수 있음)")
            else:
                # CSV: 인코딩 자동 재시도 (utf-8-sig → utf-8 → cp949 → euc-kr)
                encodings = ["utf-8-sig", "utf-8", "cp949", "euc-kr"]
                for enc in encodings:
                    try:
                        file.seek(0)
                        df = pd.read_csv(file, encoding=enc)
                        st.caption(f"인코딩 감지: {enc}")
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    file.seek(0)
                    df = pd.read_csv(file, encoding="cp949", errors="ignore")
                    st.warning("정확한 인코딩 감지 실패 → 일부 문자를 건너뛰어 읽었습니다.")
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")
        st.stop()

if df is not None:
    st.write("행/열:", df.shape)
    st.dataframe(df.head())

    st.subheader("기본 통계")
    try:
        st.write(df.describe(numeric_only=True))
    except Exception:
        st.info("숫자형 컬럼이 적어 기본 통계를 건너뜁니다.")

    numeric = df.select_dtypes("number")
    if not numeric.empty:
        st.subheader("숫자형 컬럼 라인 차트")
        st.line_chart(numeric)
    else:
        st.info("숫자형 컬럼이 없어 차트를 생략합니다.")
else:
    st.info("CSV/XLSX 파일을 업로드하면 미리보기가 표시됩니다.")

st.divider()

# ===========================================
# 2) DB 불러오기(AM/PM 평균속도 지표) 섹션
# ===========================================
st.header("② DB 불러오기(AM/PM 평균속도)")

st.caption("예상 스키마: logs_road(date TEXT 'YYYYMMDD', hour INT 0-23, speed REAL, section/link_id 선택)")

colA, colB = st.columns([2, 1])
with colA:
    db_path = st.text_input("SQLite DB 경로", "data/app.db")
with colB:
    days = st.number_input("조회 일수(최근 n일)", min_value=1, max_value=30, value=7, step=1)

load_btn = st.button("DB 불러오기")

if load_btn:
    try:
        with sqlite3.connect(db_path) as conn:
            # 최근 n일 AM/PM 평균속도 (낮을수록 정체 심함)
            q = f"""
            WITH base AS (
              SELECT
                date,
                CASE
                  WHEN CAST(hour AS INT) BETWEEN 7 AND 9  THEN 'AM'
                  WHEN CAST(hour AS INT) BETWEEN 17 AND 19 THEN 'PM'
                END AS band,
                CAST(speed AS REAL) AS speed
              FROM logs_road
              WHERE date >= strftime('%Y%m%d','now','-{days} day')
            )
            SELECT band, ROUND(AVG(speed),1) AS avg_speed, COUNT(*) AS n
            FROM base
            WHERE band IS NOT NULL
            GROUP BY band
            """
            ampm = pd.read_sql_query(q, conn)

            meta = pd.read_sql_query("""
              SELECT MAX(date) AS latest_date, COUNT(*) AS total_rows
              FROM logs_road
            """, conn)

        # 메트릭 카드
        c1, c2, c3 = st.columns(3)
        latest = meta.iloc[0]["latest_date"] if not meta.empty else None
        total = int(meta.iloc[0]["total_rows"]) if not meta.empty else 0
        c1.metric("최근 적재일", latest if pd.notna(latest) else "-")
        c2.metric("누적 행수", f"{total:,}")

        if not ampm.empty:
            d = ampm.set_index("band")["avg_speed"].to_dict()
            am = d.get("AM", "-")
            pm = d.get("PM", "-")
            c3.metric("평균속도 (km/h)", f"AM: {am} / PM: {pm}")
            st.subheader("AM/PM 평균속도 막대차트")
            st.bar_chart(ampm.set_index("band")["avg_speed"])
        else:
            c3.metric("평균속도 (km/h)", "-")
            st.info("조회 구간에 해당하는 데이터가 없습니다. (테이블/날짜 범위 확인)")

    except Exception as e:
        st.error(f"DB 로드 오류: {e}")
        st.caption("• 경로가 맞는지 • logs_road 테이블이 있는지 • 컬럼(date/hour/speed) 형식이 맞는지 확인하세요.")

st.divider()

# =========================
# 3) 안내/출처
# =========================
with st.expander("출처 및 동작 개요 보기"):
    st.markdown("""
- **데이터 출처(도로 소통 속도/혼잡)**: 서울시 교통 공공데이터(T-DATA/TOPIS 계열).
- **지표 해석**: 속도(km/h)가 **낮을수록** 정체가 심함.  
- **파이프라인**:  
  - ETL 레포(`project-etl-sql`)가 매일 데이터 수집 → `data/raw/road_YYYYMMDD.csv` 저장 → `data/app.db`의 `logs_road`로 누적 적재  
  - 본 대시보드에서 `DB 불러오기`로 최근 n일 **AM(07–09)/PM(17–19)** 평균속도 카드/차트 표시
""")
