.DEFAULT_GOAL := help
BOOTSTRAP_PYTHON ?= python3
PYTHON ?= .venv/bin/python
NPM ?= npm
export PYTHONPATH := .:ml/src

.PHONY: help setup setup-integrations lint format test test-ml test-backend test-frontend sample-artifacts validate-artifacts schemas openapi types types-official api-check dev up down clean typecheck docs-check

help:
	@printf '%s\n' 'setup                 Install the base Python and frontend dependencies' \
	  'setup-integrations    Install the pinned chart and optional tooling packages' \
	  'lint                  Run Ruff and ESLint' 'format                Apply Ruff formatting' \
	  'typecheck             Check Python and TypeScript' 'test                  Run all unit suites' \
	  'test-ml               Run ML utility and reproducibility tests' \
	  'test-backend          Run the placeholder API tests' 'test-frontend         Run dashboard unit tests' \
	  'schemas               Export artifact JSON Schemas' 'sample-artifacts      Generate seeded sample artifacts' \
	  'validate-artifacts    Validate all sample artifact schemas' 'openapi               Export the HTTP contract' \
	  'types                 Generate dashboard types from OpenAPI' \
	  'types-official        Check the contract with openapi-typescript' \
	  'docs-check            Validate local links, terms, and roadmap coverage' \
	  'api-check             Exercise the running backend over HTTP' \
	  'dev                   Start the API and dashboard locally' \
	  'up / down             Start or stop the Compose stack' 'clean                 Remove local build caches'

setup:
	$(BOOTSTRAP_PYTHON) -m venv .venv
	$(PYTHON) -m pip install -r ml/requirements/dev.txt -r backend/requirements.txt -e ml
	$(NPM) --prefix frontend ci --legacy-peer-deps

setup-integrations:
	$(NPM) --prefix frontend run setup:integrations

lint:
	$(PYTHON) -m ruff check ml backend scripts
	$(PYTHON) -m ruff format --check ml backend scripts
	$(NPM) --prefix frontend run lint

format:
	$(PYTHON) -m ruff check --fix ml backend scripts
	$(PYTHON) -m ruff format ml backend scripts

typecheck:
	$(PYTHON) -m mypy ml/src backend/app
	$(NPM) --prefix frontend run typecheck

test: test-ml test-backend test-frontend

test-ml:
	$(PYTHON) -m pytest -q ml/tests

test-backend:
	$(PYTHON) -m pytest -q backend/tests

test-frontend:
	$(NPM) --prefix frontend test

schemas:
	$(PYTHON) -m needlecast_ml.cli export-schemas

sample-artifacts:
	$(PYTHON) -m needlecast_ml.cli make-sample-artifacts

validate-artifacts:
	$(PYTHON) -m needlecast_ml.cli validate-artifacts

openapi:
	$(PYTHON) -m backend.scripts.export_openapi

types: openapi
	$(PYTHON) scripts/export_types.py

types-official: openapi
	$(NPM) --prefix frontend run types:official

docs-check:
	$(PYTHON) scripts/check_docs.py

api-check:
	$(PYTHON) scripts/api_smoke.py

dev:
	@set -eu; \
	$(PYTHON) -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --no-access-log & api=$$!; \
	trap 'kill "$$api" 2>/dev/null || true' EXIT; \
	trap 'exit 130' INT; trap 'exit 143' TERM; \
	$(NPM) --prefix frontend run dev -- --hostname 127.0.0.1

up:
	docker compose up --build

down:
	docker compose down

clean:
	rm -rf frontend/.next frontend/coverage .pytest_cache .mypy_cache .ruff_cache
