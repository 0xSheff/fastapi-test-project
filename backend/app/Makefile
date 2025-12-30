ALEMBIC = alembic
BACKEND_CONTAINER = backend1

PHONY: mm m

mm:
	${ALEMBIC} revision --autogenerate -m ${msg}

m:
	${ALEMBIC} upgrade head
