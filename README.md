# 서울 출퇴근 EDA 대시보드 (Streamlit + SQLite)

[![Python](https://img.shields.io/badge/Python-3.x-informational?logo=python)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-app-lightgrey?logo=streamlit)]()
[![SQLite](https://img.shields.io/badge/SQLite-db-blue?logo=sqlite)]()
[![Last Commit](https://img.shields.io/github/last-commit/cxo-ca/project-eda-dashboard)]()
![Issues](https://img.shields.io/github/issues/cxo-ca/project-eda-dashboard)
![Stars](https://img.shields.io/github/stars/cxo-ca/project-eda-dashboard)
[![License](https://img.shields.io/badge/license-MIT-green)]()

**배포 URL:** https://project-eda-dashboard-mdymcubfvmcmtygcqisq98.streamlit.app/  

CSV/XLSX 업로드로 **기본 EDA(요약/차트)** 를 보여주고, SQLite(`logs_road`)가 있으면 **최근 n일 AM(07–09) / PM(17–19) 평균속도 지표**를 카드/차트로 표시합니다. :contentReference[oaicite:0]{index=0}

---

## Quickstart (3분 내 실행)

### 1) 설치
```bash
pip install -r requirements.txt
```

### 2) 실행(로컬)
```bash
python -m streamlit run app/app.py
```

### 3) 결과 확인
- 브라우저에서 Streamlit UI가 열립니다.
- 기본 DB는 ./data/app.db (레포 내부) 입니다.
- CSV/XLSX 업로드 시 자동 인코딩 재시도 후 기본 통계/차트를 확인할 수 있습니다.

## Results (무엇이 보이나)
### Output
- AM/PM 평균속도 카드 (최근 n일 기준)
- AM/PM 평균속도 막대차트
- CSV/XLSX 업로드 기반 EDA: shape, describe, 숫자형 라인 차트 등

### Screenshot
<img width="940" height="383" alt="image" src="https://github.com/user-attachments/assets/d6750d4f-e6dc-4be2-93af-d24b34be38b6" />
<img width="940" height="295" alt="image" src="https://github.com/user-attachments/assets/9403d345-1d3d-4bfd-b45e-816ee1629d9e" />
<img width="940" height="264" alt="image" src="https://github.com/user-attachments/assets/45284e06-16f0-4049-b742-7bdc9070e66c" />

## 사용법
1. 파일 업로드
- CSV/XLSX 업로드 → 자동 인코딩 감지(utf-8/cp949 등) → 기본 통계/차트 표시
2. DB 불러오기
- SQLite DB 경로 입력 → ‘DB 불러오기’ 클릭
- logs_road가 있으면 최근 n일 AM/PM 평균속도를 계산합니다.

## DB 스키마
```bash
logs_road(
  date  TEXT    -- 'YYYYMMDD'
  hour  INTEGER -- 0~23
  speed REAL    -- km/h (낮을수록 혼잡)
)
```

## 트러블슈팅
- unable to open database file  
경로/부모폴더 확인, data/app.db 권장
- no such table: logs_road  
ETL로 적재가 안 됐거나 다른 DB를 보고 있는 상태입니다(경로 통일)

## About
목적: 공개데이터 기반 EDA + 지표 정의(AM/PM 평균속도) + 대시보드 구현
