run-build:
	docker compose up --build -d

dispose:
	docker compose down -v
