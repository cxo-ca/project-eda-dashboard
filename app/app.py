file = st.file_uploader("CSV 또는 XLSX 업로드", type=["csv", "xlsx"])
if file:
    name = file.name.lower()
    try:
        if name.endswith(".xlsx"):
            # 엑셀은 인코딩 이슈 없음 (openpyxl 필요)
            df = pd.read_excel(file)
        else:
            # CSV: 인코딩 자동 재시도 (utf-8 → cp949 → euc-kr)
            encodings = ["utf-8", "cp949", "euc-kr"]
            last_err = None
            for enc in encodings:
                try:
                    file.seek(0)              # 재시도 전에 파일 포인터 리셋
                    df = pd.read_csv(file, encoding=enc)
                    st.caption(f"인코딩 감지: {enc}")
                    break
                except UnicodeDecodeError as e:
                    last_err = e
                    continue
            else:
                raise last_err  # 모두 실패하면 에러로 처리

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()

    # 이하 기존 로직 유지
    st.write("행/열:", df.shape)
    st.dataframe(df.head())
    numeric = df.select_dtypes("number")
    if not numeric.empty:
        st.line_chart(numeric)
    else:
        st.info("숫자형 컬럼이 없어 차트를 생략합니다.")
else:
    st.info("CSV/XLSX를 올리면 바로 확인할 수 있어요.")
