flask-debug:
	uvx flask --app gameplot run --debug

build:
	docker compose build

up:
	docker compose up --build --remove-orphans

down:
	docker compose down

watch:
	docker compose watch

reset-db: down build
	docker compose up db -d
	docker compose run web flask init-db

logs:
	docker compose logs -f

.PHONY: flask-debug build up watch reset-db logs down