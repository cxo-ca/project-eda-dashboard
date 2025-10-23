# Streamlit Cloud가 레포 루트에서 기본으로 찾는 진입점 파일.
# 설정 없이도 app/app.py를 실행하게 해줍니다.
import os, runpy

BASE_DIR = os.path.dirname(__file__)
ENTRY = os.path.join(BASE_DIR, "app", "app.py")

if not os.path.exists(ENTRY):
    raise FileNotFoundError(f"Entry not found: {ENTRY}")
runpy.run_path(ENTRY, run_name="__main__")
