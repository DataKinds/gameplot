debug:
	uvx flask --app gameplot run --debug

compose-build:
	docker compose watch --build --remove-orphans

watch:
	docker compsoe watch