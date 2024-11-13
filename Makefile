install:
	 cd app && pip3 install -r requirements.txt
prep:
	 cd app && python3 prep_data.py
run:
	 cd app && PYTHONPATH=../.. python3 -m main
test:
	 cd app && pytest evals.py -v

# dev
dev:
	uvicorn app.main:app --reload
up:
	docker compose --env-file app/.env up --build
build:
	docker compose build
	 