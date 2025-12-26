DC = docker compose

PHONY: up

up:
	${DC} up -d --remove-orphans

down:
	${DC} down