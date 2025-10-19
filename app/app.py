import streamlit as st
import pandas as pd

st.title("공개데이터 EDA 대시보드 (초안)")
st.write("CSV/XLSX를 업로드하면 기본 통계/차트를 보여줍니다.")

file = st.file_uploader("CSV 또는 XLSX 업로드", type=["csv", "xlsx"])
if file:
    name = file.name.lower()
    try:
        if name.endswith(".xlsx"):
            df = pd.read_excel(file)  # openpyxl 필요
        else:
            df = pd.read_csv(file)
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()

    st.write("행/열:", df.shape)
    st.dataframe(df.head())

    numeric = df.select_dtypes("number")
    if not numeric.empty:
        st.line_chart(numeric)
    else:
        st.info("숫자형 컬럼이 없어 차트를 생략합니다.")
else:
    st.info("CSV/XLSX를 올리면 바로 확인할 수 있어요.")
