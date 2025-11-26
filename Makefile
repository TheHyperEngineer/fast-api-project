# Makefile with common development tasks
PY ?= python
PIP ?= pip

.PHONY: install build up down seed test integration test-integration run run-dev image

install:
	$(PY) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

build:
	docker build -t hello-world:latest .

image: build

up:
	docker compose up --build -d

down:
	docker compose down --volumes --remove-orphans

run:
	python -m uvicorn app.main:app --reload --port 8005 --log-level debug

run-dev: install
	$(PY) -m uvicorn app.main:app --reload --port 8005 --log-level debug

seed:
	# seed locally against a running Mongo (expect MONGO_URI env var set)
	$(PY) seed_db.py

test: install
	pytest -q

integration:
	# Start compose, run seeding, and test endpoints via pytest
	docker compose up --build -d
	sleep 2
	pip install -r requirements.txt
	pytest -q tests/integration
	docker compose down --volumes --remove-orphans
