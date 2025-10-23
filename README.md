**배포 URL:** https://project-eda-dashboard-mdymcubfvmcmtygcqisq98.streamlit.app/  
**로컬 테스트 DB 경로:** `data/app.db`  (EDA 레포 내부 파일)

👉 [실행하기(배포)](https://project-eda-dashboard-mdymcubfvmcmtygcqisq98.streamlit.app/)
![대시보드 스크린샷](app/screenshot.png)

# 공개데이터 EDA 대시보드
👉 [실행하기(배포)](https://project-eda-dashboard-mdymcubfvmcmtygcqisq98.streamlit.app/) · [프로필](https://github.com/cxo-ca)

![Python](https://img.shields.io/badge/Python-3.10+-informational?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-app-lightgrey)
![Pandas](https://img.shields.io/badge/Pandas-EDA-blue)


공개데이터 EDA → 출퇴근 피크 시각화, 핵심 지표 3개 정의
data-analysis, streamlit, python, dashboard

EDA: Public data EDA → peak commute visualization, 3 key metrics

## 실행 방법
```bash
pip install -r requirements.txt
streamlit run app/app.py

## 결과
- CSV/XLSX 업로드 → 자동 인코딩 감지(utf-8/cp949 등), 핵심 지표/차트 **즉시 표시**

## 데이터 출처
- 도로 소통 속도/혼잡: 서울시 교통 관련 공공데이터(Open API, T-DATA/TOPIS 계열).
- 본 프로젝트의 AM(07–09)/PM(17–19) 지표는 시간대 평균 속도를 이용합니다.
- 속도(km/h)가 **낮을수록 정체가 심함**을 의미합니다.

## 동작 개요
- ETL(`project-etl-sql`): 매일 도로 속도 데이터를 수집 → `data/raw/road_YYYYMMDD.csv` 저장 → `data/app.db`의 `logs_road` 테이블로 누적 적재.
- EDA(`project-eda-dashboard`): 상단 “DB 불러오기”에서 `data/app.db` 경로 입력 → 최근 n일 AM/PM 평균속도 카드/차트 표시.
