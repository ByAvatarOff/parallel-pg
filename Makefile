.PHONY: all

SHELL=/bin/bash -e

DCF_LOCAL = docker compose -f docker-compose.yml

build:
	${DCF_LOCAL} build

up:
	${DCF_LOCAL} up -d

down:
	${DCF_LOCAL} down --remove-orphans