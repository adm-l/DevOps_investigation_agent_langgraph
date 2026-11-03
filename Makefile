.PHONY: install run test lint compose-up compose-down
install:
	python3.12 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
test:
	pytest -q
lint:
	ruff check .
compose-up:
	docker compose up --build
compose-down:
	docker compose down
