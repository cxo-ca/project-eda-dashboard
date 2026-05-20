# 서울 출퇴근 EDA 대시보드

> 서울 출퇴근 시간대 교통 데이터를 분석하고, AM/PM 평균속도 지표를 Streamlit 대시보드로 시각화한 프로젝트입니다.

![Python](https://img.shields.io/badge/Python-3.x-informational?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-lightgrey?logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-database-blue?logo=sqlite)
![Last Commit](https://img.shields.io/github/last-commit/cxo-ca/project-eda-dashboard)
![Issues](https://img.shields.io/github/issues/cxo-ca/project-eda-dashboard)
![Stars](https://img.shields.io/github/stars/cxo-ca/project-eda-dashboard)

## Demo

- 배포 URL: https://project-eda-dashboard-mdymcubfvmcmtygcqisq98.streamlit.app/

---

## 프로젝트 개요

이 프로젝트는 단순히 데이터를 시각화하는 것이 아니라, 출퇴근 시간대 교통 흐름을 빠르게 파악할 수 있도록 핵심 지표를 정의하고 대시보드로 구현하는 것을 목표로 했습니다.

CSV/XLSX 파일을 업로드하면 기본 EDA 결과를 확인할 수 있고, SQLite 데이터베이스에 `logs_road` 테이블이 존재하면 최근 n일 기준 AM/PM 평균속도 지표를 카드와 차트로 확인할 수 있습니다.

---

## 문제 정의

출퇴근 시간대 교통 데이터는 시간대별로 차이가 크기 때문에 전체 평균만 보면 혼잡 패턴을 파악하기 어렵습니다.

따라서 이 프로젝트에서는 다음 질문에 답하는 것을 목표로 했습니다.

- 출근 시간대와 퇴근 시간대의 평균속도는 어떻게 다른가?
- 최근 n일 기준으로 AM/PM 교통 흐름을 빠르게 비교할 수 있는가?
- 업로드한 CSV/XLSX 데이터를 별도 전처리 없이 바로 탐색할 수 있는가?

---

## 핵심 기능

| 기능 | 설명 |
|---|---|
| CSV/XLSX 업로드 | 사용자가 직접 파일을 업로드해 기본 EDA 수행 |
| 자동 인코딩 처리 | `utf-8`, `cp949` 등 주요 인코딩 재시도 |
| 기본 통계 확인 | 데이터 shape, 컬럼 정보, 기술통계 확인 |
| 숫자형 차트 | 숫자형 컬럼 기반 라인 차트 생성 |
| SQLite 연동 | `logs_road` 테이블이 있으면 교통 지표 계산 |
| AM/PM KPI 카드 | 출근/퇴근 시간대 평균속도 비교 |
| 최근 n일 필터 | 분석 기간을 사용자가 조정 가능 |

---

## 분석 지표

| 지표 | 정의 | 해석 |
|---|---|---|
| AM 평균속도 | 07시~09시 평균속도 | 낮을수록 출근 시간대 혼잡 가능성 증가 |
| PM 평균속도 | 17시~19시 평균속도 | 낮을수록 퇴근 시간대 혼잡 가능성 증가 |
| 최근 n일 평균 | 사용자가 선택한 기간의 평균속도 | 단기 교통 흐름 비교에 활용 |

---

## 기술 스택

| 구분 | 사용 기술 |
|---|---|
| Language | Python |
| Dashboard | Streamlit |
| Database | SQLite |
| Data Handling | Pandas |
| Visualization | Streamlit Chart |
| Deployment | Streamlit Community Cloud |

---

## 폴더 구조

~~~text
project-eda-dashboard/
├── app/
│   └── app.py
├── data/
│   └── app.db
├── streamlit_app.py
├── requirements.txt
├── Makefile
└── README.md
~~~

---

## Quickstart

### 1. 패키지 설치

~~~bash
pip install -r requirements.txt
~~~

### 2. 로컬 실행

~~~bash
python -m streamlit run app/app.py
~~~

또는 Streamlit Cloud 배포용 진입 파일을 실행할 수 있습니다.

~~~bash
python -m streamlit run streamlit_app.py
~~~

### 3. 결과 확인

브라우저에서 Streamlit UI가 열리면 CSV/XLSX 파일을 업로드하거나 SQLite DB 경로를 입력해 대시보드를 확인합니다.

---

## 사용 방법

### 1. 파일 업로드 기반 EDA

CSV 또는 XLSX 파일을 업로드하면 다음 결과를 확인할 수 있습니다.

- 데이터 크기
- 컬럼 목록
- 결측치 여부
- 기술통계
- 숫자형 컬럼 차트

### 2. SQLite 기반 교통 지표 확인

SQLite DB 경로를 입력하고 `logs_road` 테이블이 존재하면 다음 결과를 확인할 수 있습니다.

- 최근 n일 AM 평균속도
- 최근 n일 PM 평균속도
- AM/PM 평균속도 비교 차트

---

## DB 스키마

~~~sql
logs_road (
    date  TEXT,     -- YYYYMMDD
    hour  INTEGER,  -- 0~23
    speed REAL      -- km/h, 낮을수록 혼잡
);
~~~

---

## 화면 예시

### CSV/XLSX 업로드 EDA

업로드한 데이터의 기본 구조와 통계 정보를 확인할 수 있습니다.

### AM/PM 평균속도 KPI

출근 시간대와 퇴근 시간대의 평균속도를 카드 형태로 비교할 수 있습니다.

### 평균속도 비교 차트

최근 n일 기준 AM/PM 평균속도 차이를 시각적으로 확인할 수 있습니다.

---

## 트러블슈팅

### `unable to open database file`

SQLite DB 경로가 잘못되었거나 부모 폴더가 존재하지 않을 때 발생할 수 있습니다.

해결 방법:

- `data/app.db` 경로가 존재하는지 확인
- DB 파일이 실제로 생성되어 있는지 확인
- 상대경로와 절대경로를 다시 확인

### `no such table: logs_road`

현재 연결한 SQLite DB 안에 `logs_road` 테이블이 없을 때 발생합니다.

해결 방법:

- ETL 스크립트로 데이터가 정상 적재되었는지 확인
- 연결한 DB 파일이 올바른 파일인지 확인
- 테이블명이 `logs_road`와 일치하는지 확인

---

## 프로젝트에서 보여주고자 한 역량

- 공개데이터 기반 EDA 수행
- 분석 목적에 맞는 KPI 정의
- Streamlit을 활용한 데이터 대시보드 구현
- SQLite 기반 데이터 조회 및 지표 계산
- 사용자가 직접 데이터를 업로드해 탐색할 수 있는 인터페이스 구현
- 분석 결과를 포트폴리오 형태로 구조화하는 능력

---

## 향후 개선 방향

- 날짜별 평균속도 추이 차트 추가
- 요일별 출퇴근 속도 비교
- 구간별 혼잡도 랭킹 추가
- 업로드 데이터 컬럼 자동 추천 기능 추가
- ETL 프로젝트와 연동 구조 고도화
