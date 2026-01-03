DC = docker compose
BACKEND_CONTAINER = backend1

PHONY: up down restart build shell test

up:
	${DC} up -d --remove-orphans

down:
	${DC} down

restart:
	${DC} down
	${DC} up -d --remove-orphans

build:
	${DC} build

shell:
	${DC} exec -it ${BACKEND_CONTAINER} bash

test:
	${DC} exec -it ${BACKEND_CONTAINER} pytest --cov=app tests/