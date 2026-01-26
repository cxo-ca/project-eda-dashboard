PY=python

install:
	$(PY) -m pip install -r requirements.txt

run:
	$(PY) -m streamlit run app/app.py

lint:
	$(PY) -m pip install ruff
	$(PY) -m ruff check .

test:
	$(PY) -m pip install pytest
	$(PY) -m pytest -q
