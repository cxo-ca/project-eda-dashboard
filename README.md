# 서울 출퇴근 EDA 대시보드

[![Python](https://img.shields.io/badge/Python-3.x-informational?logo=python)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-app-lightgrey?logo=streamlit)]()
[![SQLite](https://img.shields.io/badge/SQLite-db-blue?logo=sqlite)]()
[![Last Commit](https://img.shields.io/github/last-commit/cxo-ca/project-eda-dashboard)]()
![Issues](https://img.shields.io/github/issues/cxo-ca/project-eda-dashboard)
![Stars](https://img.shields.io/github/stars/cxo-ca/project-eda-dashboard)
[![License](https://img.shields.io/badge/license-MIT-green)]()

**배포 URL:** https://project-eda-dashboard-mdymcubfvmcmtygcqisq98.streamlit.app/  
**로컬 테스트 DB 경로:** `data/app.db` (이 레포 내부 파일)

> CSV/XLSX 업로드 미리보기 + SQLite에서 최근 **AM(07–09) / PM(17–19)** 평균속도 카드/차트 표시

---

## Quickstart (3분 내 실행)

### 1) 설치
```bash
pip install -r requirements.txt
```

### 2) 실행
```bash
# 로컬 실행
python -m streamlit run app/app.py
```

### 3) 결과 확인
- 브라우저에서 Streamlit UI가 열립니다.
- data/app.db가 있으면 DB 기반 지표/차트가 표시됩니다.
- CSV/XLSX 업로드 시 자동 인코딩 감지 후 기본 통계/차트를 확인할 수 있습니다.

## Results (무엇이 보이나)
### Output
- 최근 기간 기준 AM(07–09) / PM(17–19) 평균속도 카드
- 시간대별 속도 분포/추이 차트
- CSV/XLSX 업로드 기반 EDA(기본 통계/차트) 또는 DB 기반 조회

### Screenshot
(여기에 기존 README의 스크린샷 1~2개를 넣으세요)

## 사용법
1. 파일 업로드
- CSV/XLSX 업로드 → 자동 인코딩 감지(utf-8/cp949 등) → 기본 통계/차트 표시

2. DB 불러오기
- 입력칸에 data/app.db 유지 → ‘DB 불러오기’ 클릭

## 스키마
```bash
logs_road(
  date  TEXT    -- 'YYYYMMDD'
  hour  INTEGER -- 0~23
  speed REAL    -- km/h (낮을수록 혼잡)
)
```

### 트러블슈팅
- unable to open database file  
경로/부모폴더 확인, data/app.db 권장
- no such table: logs_road  
ETL로 적재하거나, logs(timestamp,value)가 있으면 앱이 자동 변환되는지 확인
- 데이터 없음  
조회 일수 늘리기(예: 30), AM/PM 시간대 데이터 포함 여부 확인
