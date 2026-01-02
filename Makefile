DC = docker compose
BACKEND_CONTAINER = backend1

PHONY: up down build shell test

up:
	${DC} up -d --remove-orphans

down:
	${DC} down

build:
	${DC} build

shell:
	${DC} exec -it ${BACKEND_CONTAINER} bash

test:
	${DC} exec -it ${BACKEND_CONTAINER} pytest --cov=app tests/