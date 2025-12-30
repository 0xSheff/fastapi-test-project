DC = docker compose
BACKEND_CONTAINER = backend1

PHONY: up down build shell

up:
	${DC} up -d --remove-orphans

down:
	${DC} down

build:
	${DC} build

shell:
	${DC} exec -it ${BACKEND_CONTAINER} bash