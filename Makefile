run-build:
	docker compose up --build -d

shutdown:
	docker compose down

demolish:
	docker compose down -v

load:
	python ./load_producer/loader.py
