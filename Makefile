# Makefile generated with pymakefile
help:
	@grep -E '^[A-Za-z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "[36m%-30s[0m %s\n", $$1, $$2}'

ps:
	docker-compose ps

build-app:
	docker-compose build app

build-worker:
	docker-compose build worker

up:
	docker-compose up

stop:
	docker-compose stop

stop-celery:
	docker-compose stop worker

logs-db:
	docker-compose logs -f

logs-db:
	docker-compose logs -f db

logs-app:
	docker-compose logs -f app

logs-worker:
	docker-compose logs -f worker

exec-app:
	docker-compose run --rm app bash

migrate:
	docker-compose run --rm app python manage.py migrate

migrations:
	docker-compose run --rm app python manage.py makemigrations

tests:
	docker-compose run --rm app coverage run --source='.' manage.py test
	docker-compose run --rm app coverage report

lint:
	docker-compose exec app black .
	docker-compose exec app isort . --profile black

fixtures:
	docker-compose run --rm app python fixtures.py
