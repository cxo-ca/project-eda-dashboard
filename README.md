# 서울 출퇴근 EDA 대시보드

**배포 URL:** https://project-eda-dashboard-mdymcubfvmcmtygcqisq98.streamlit.app/  
**로컬 테스트 DB 경로:** `data/app.db`  (이 레포 내부 파일)

> CSV/XLSX 업로드 미리보기 + SQLite에서 최근 **AM(07–09) / PM(17–19)** 평균속도 카드/차트 표시

## 빠른 실행
```bash
pip install -r requirements.txt
streamlit run app/app.py

사용법
① 파일 업로드: CSV/XLSX → 자동 인코딩 감지(utf-8/cp949 등), 기본 통계/차트 표시
② DB 불러오기: 입력칸에 data/app.db 두고 DB 불러오기 클릭

스키마
logs_road(
  date  TEXT    -- 'YYYYMMDD'
  hour  INTEGER -- 0~23
  speed REAL    -- km/h (낮을수록 혼잡)
)

트러블슈팅
unable to open database file → 경로/부모폴더 확인, data/app.db 권장
no such table: logs_road → ETL로 적재 또는 logs(timestamp,value)가 있으면 앱이 자동 변환
데이터 없음 → 조회 일수 늘리기(예: 30), AM/PM 시간대 데이터 포함 확인
