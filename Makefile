flask-debug:
	uvx flask --app gameplot run --debug

build:
	docker compose build

up:
	docker compose up --build --remove-orphans

down:
	docker compose down

watch:
	-xdg-open http://127.0.0.1:5000/
	docker compose watch

reset-db: 
	docker compose down db web
	docker compose up --build --remove-orphans -d db web
	docker compose run web flask reset-db
	docker compose run web flask seed-db

logs:
	docker compose logs -f

shell: 
	docker compose exec web flask shell

.PHONY: flask-debug build up watch reset-db logs down shell