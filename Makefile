debug:
	uvx flask --app gameplot run --debug

compose-build:
	docker compose up --build --remove-orphans