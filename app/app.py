import streamlit as st
import pandas as pd

st.title("공개데이터 EDA 대시보드 (초안)")
st.write("CSV/XLSX 업로드 → 기본 통계/차트 표시")

# 1) 파일 업로더 + 강제 CP949 옵션
file = st.file_uploader("CSV 또는 XLSX 업로드", type=["csv", "xlsx"])
force_cp949 = st.checkbox("강제 CP949로 읽기(윈도우 CSV 오류 시)")

if file:
    name = file.name.lower()
    try:
        if name.endswith(".xlsx"):
            # XLSX는 인코딩 이슈 없음 (openpyxl 필요)
            df = pd.read_excel(file)
            st.caption("형식: XLSX (인코딩 문제 없음)")
        else:
            # CSV 읽기
            if force_cp949:
                # 사용자가 강제로 CP949 선택한 경우
                file.seek(0)
                df = pd.read_csv(file, encoding="cp949", errors="ignore")
                st.caption("강제 인코딩: cp949 (일부 문자를 무시할 수 있음)")
            else:
                # 자동 감지 시도: utf-8-sig → utf-8 → cp949 → euc-kr
                encodings = ["utf-8-sig", "utf-8", "cp949", "euc-kr"]
                last_err = None
                for enc in encodings:
                    try:
                        file.seek(0)  # 재시도 전 포인터 리셋
                        df = pd.read_csv(file, encoding=enc)
                        st.caption(f"인코딩 감지: {enc}")
                        break
                    except UnicodeDecodeError as e:
                        last_err = e
                        continue
                else:
                    # 전부 실패하면 어떻게든 열기
                    file.seek(0)
                    df = pd.read_csv(file, encoding="cp949", errors="ignore")
                    st.warning("정확한 인코딩 감지 실패 → 일부 문자를 건너뛰어 읽었습니다.")
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")
        st.stop()

    # 2) 미리보기/기본 통계/차트
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
    st.info("CSV/XLSX 파일을 업로드해 주세요.")
