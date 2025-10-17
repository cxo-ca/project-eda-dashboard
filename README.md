공개데이터 EDA → 출퇴근 피크 시각화, 핵심 지표 3개 정의
https://sites.google.com/view/cxo-ca  (또는 추후 Streamlit 주소)
data-analysis, streamlit, python, dashboard

EDA: Public data EDA → peak commute visualization, 3 key metrics

# EDA 레포
git clone git@github.com:cxo-ca/project-eda-dashboard.git
cd project-eda-dashboard

python -m venv .venv
# Win: . .venv/Scripts/activate | macOS/Linux: source .venv/bin/activate
pip install pandas numpy matplotlib plotly streamlit jupyter
pip freeze > requirements.txt

mkdir -p app data notebooks
cat > app/app.py << 'PY'
import streamlit as st, pandas as pd
st.title("공개데이터 EDA 대시보드 (초안)")
file = st.file_uploader("CSV 업로드", type=["csv"])
if file:
    df = pd.read_csv(file)
    st.write("행/열:", df.shape)
    st.dataframe(df.head())
    st.line_chart(df.select_dtypes("number"))
else:
    st.info("CSV를 업로드하면 기본 통계/차트를 볼 수 있어요.")
PY

printf ".venv/\n__pycache__/\n.ipynb_checkpoints/\n*.env\n*.DS_Store\n" > .gitignore

git add requirements.txt app/.gitignore app/app.py .gitignore || true
git add requirements.txt app/app.py .gitignore
git commit -m "feat(app): Streamlit 기본 화면/CSV 업로드 추가"
git push
