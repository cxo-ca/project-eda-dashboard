# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

st.title("EDA Day3")
st.write("CSV/XLSX 업로드 → 통계/기간 필터/지표/차트 제공")

# ── 업로드 + 인코딩 옵션 ─────────────────────────────────────────
file = st.file_uploader("CSV 또는 XLSX 업로드", type=["csv", "xlsx"])
force_cp949 = st.checkbox("강제 CP949로 읽기(윈도우 CSV 오류 시)")

df = None
if file:
    name = file.name.lower()
    try:
        if name.endswith(".xlsx"):
            # XLSX는 인코딩 문제 없음 (openpyxl 필요)
            df = pd.read_excel(file)
            st.caption("형식: XLSX (인코딩 문제 없음)")
        else:
            if force_cp949:
                file.seek(0)
                df = pd.read_csv(file, encoding="cp949", errors="ignore")
                st.caption("강제 인코딩: cp949 (일부 문자를 무시할 수 있음)")
            else:
                # CSV 인코딩 자동 재시도
                for enc in ["utf-8-sig", "utf-8", "cp949", "euc-kr"]:
                    try:
                        file.seek(0)
                        df = pd.read_csv(file, encoding=enc)
                        st.caption(f"인코딩 감지: {enc}")
                        break
                    except UnicodeDecodeError:
                        pass
                else:
                    file.seek(0)
                    df = pd.read_csv(file, encoding="cp949", errors="ignore")
                    st.warning("정확한 인코딩 감지 실패 → 일부 문자를 무시하고 읽었습니다.")
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")
        st.stop()

if df is None:
    st.info("CSV/XLSX 파일을 업로드해 주세요.")
    st.stop()

# ── 미리보기 ─────────────────────────────────────────────────────
st.write("행/열:", df.shape)
st.dataframe(df.head())

# ── 기본 통계 ────────────────────────────────────────────────────
st.subheader("기본 통계")
try:
    st.write(df.describe(numeric_only=True))
except Exception:
    st.info("숫자형 컬럼이 적어 기본 통계를 건너뜁니다.")

# ── 날짜 컬럼 자동 인식 + 기간 필터 ─────────────────────────────
date_filtered = df.copy()
detected_date_col = None
for c in df.columns:
    if "date" in c.lower() or "time" in c.lower():
        try:
            date_col = pd.to_datetime(df[c])
            detected_date_col = c
            st.caption(f"날짜 컬럼 인식: {c}")
            start, end = date_col.min(), date_col.max()
            # 시작/끝이 같을 수 있어 기본 범위 안전 처리
            left = start.to_pydatetime() if hasattr(start, "to_pydatetime") else pd.to_datetime(start).to_pydatetime()
            right = end.to_pydatetime() if hasattr(end, "to_pydatetime") else pd.to_datetime(end).to_pydatetime()
            sel = st.slider("기간 선택", min_value=left, max_value=right, value=(left, right))
            mask = (date_col >= sel[0]) & (date_col <= sel[1])
            date_filtered = df.loc[mask].reset_index(drop=True)
            break
        except Exception:
            continue

# ── 숫자 컬럼 선택 + 지표 카드 ──────────────────────────────────
num_cols = date_filtered.select_dtypes("number").columns.tolist()
y_col = st.selectbox("차트 컬럼 선택", num_cols) if num_cols else None

c1, c2, c3 = st.columns(3)
c1.metric("행 수", len(date_filtered))
c2.metric("숫자 컬럼 수", len(num_cols))
c3.metric(f"{y_col} 평균" if y_col else "평균", round(date_filtered[y_col].mean(), 2) if y_col else "-")

# ── 차트 ─────────────────────────────────────────────────────────
st.subheader("차트")
if y_col:
    st.line_chart(date_filtered[[y_col]])
elif num_cols:
    st.line_chart(date_filtered[num_cols])
else:
    st.info("숫자형 컬럼이 없어 차트를 생략합니다.")

# ── 참고 ─────────────────────────────────────────────────────────
st.caption("※ XLSX를 읽으려면 requirements.txt에 openpyxl이 있어야 합니다.")
