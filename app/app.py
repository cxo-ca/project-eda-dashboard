import streamlit as st
import pandas as pd

st.title("공개데이터 EDA 대시보드 (초안)")
st.write("CSV를 업로드하면 기본 통계/차트를 보여줍니다.")

file = st.file_uploader("CSV 업로드", type=["csv"])
if file:
    df = pd.read_csv(file)
    st.write("행/열:", df.shape)
    st.dataframe(df.head())
    numeric = df.select_dtypes("number")
    if not numeric.empty:
        st.line_chart(numeric)
    else:
        st.info("숫자형 컬럼이 없어 차트를 생략합니다.")
else:
    st.info("CSV를 올리면 바로 확인할 수 있어요.")
