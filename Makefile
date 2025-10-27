flask-debug:
	uvx flask --app gameplot run --debug

compose-build:
	docker compose up --build --remove-orphans

watch:
	docker compose watch

init-db:
	docker compose exec web flask init-db