DC = docker compose

PHONY: up

up:
	${DC} up -d

down:
	${DC} down