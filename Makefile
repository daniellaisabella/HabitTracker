SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -ExecutionPolicy Bypass -Command

.PHONY: help install backend frontend run docker-build docker-up docker-down docker-logs docker-ps

help:
	@Write-Host "Targets:"
	@Write-Host "  make install      - Install dependencies with uv sync"
	@Write-Host "  make backend      - Start Flask backend (port 5000)"
	@Write-Host "  make frontend     - Start Streamlit frontend (port 8501)"
	@Write-Host "  make run          - Start backend + frontend in separate windows"
	@Write-Host "  make docker-build - Pull/update Docker images"
	@Write-Host "  make docker-up    - Start all services with Docker Compose"
	@Write-Host "  make docker-down  - Stop Docker Compose services"
	@Write-Host "  make docker-logs  - Follow Docker Compose logs"
	@Write-Host "  make docker-ps    - Show Docker Compose service status"

install:
	uv sync

backend:
	uv run python -m backend.main

frontend:
	uv run streamlit run frontend/app.py

run-local:
	@Start-Process -FilePath "uv" -ArgumentList "run","python","-m","backend.main"
	@Start-Process -FilePath "uv" -ArgumentList "run","streamlit","run","frontend/app.py"
	@Write-Host "Backend started on http://127.0.0.1:5000"
	@Write-Host "Frontend started on http://localhost:8501"

docker-up:
	@docker compose up

docker-build:
	@Write-Host "Pulling/updating images from registry..."
	@docker compose pull
	@Write-Host "Done. Use 'make docker-up' to start containers."

docker-down:
	@docker compose down

docker-ps:
	@docker compose ps

docker-seed:
	@docker compose exec backend python -m backend.seed

docker-db:
	@docker compose exec db psql -U postgres
	
lint:
	uv run ruff check --fix .

test:
	uv run pytest

typecheck:
	uv run pyright

pre-commit-hooks:
	uv add --dev pre-commit ruff pytest pyright
	uv run pre-commit install
	@echo "pre-commit hooks installed and ready!"