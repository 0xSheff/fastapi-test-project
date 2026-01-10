DC = docker compose
BACKEND_CONTAINER = backend1

PHONY: start stop restart build docs-up docs-restart shell test

start:
	${DC} up -d --remove-orphans

stop:
	${DC} down

restart:
	${DC} down
	${DC} up -d --remove-orphans

build:
	${DC} build

docs-up:
	${DC} --profile docs up -d --remove-orphans

docs-restart:
	${DC} restart documentation

shell:
	${DC} exec -it ${BACKEND_CONTAINER} bash

test:
	${DC} exec -it ${BACKEND_CONTAINER} pytest --cov=app tests/