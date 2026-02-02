run-build:
	docker compose up --build -d

dispose:
	docker compose down

load:
	python ./load_producer/loader.py
