SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -ExecutionPolicy Bypass -Command

PYTHON := .\.venv\Scripts\python.exe

.PHONY: help install backend frontend run docker-build docker-up docker-down docker-logs docker-ps

help:
	@Write-Host "Targets:"
	@Write-Host "  make install      - Install dependencies in .venv"
	@Write-Host "  make backend      - Start Flask backend (port 5000)"
	@Write-Host "  make frontend     - Start Streamlit frontend (port 8501)"
	@Write-Host "  make run          - Start backend + frontend in separate windows"
	@Write-Host "  make docker-build - Pull/update Docker images"
	@Write-Host "  make docker-up    - Start all services with Docker Compose"
	@Write-Host "  make docker-down  - Stop Docker Compose services"
	@Write-Host "  make docker-logs  - Follow Docker Compose logs"
	@Write-Host "  make docker-ps    - Show Docker Compose service status"

install:
	@if (-not (Test-Path "$(PYTHON)")) { throw "Missing .venv. Create it first: python -m venv .venv" }
	@& "$(PYTHON)" -m pip install -r requirements.txt

backend:
	@if (-not (Test-Path "$(PYTHON)")) { throw "Missing .venv. Create it first: python -m venv .venv" }
	@& "$(PYTHON)" -m backend.main

frontend:
	@if (-not (Test-Path "$(PYTHON)")) { throw "Missing .venv. Create it first: python -m venv .venv" }
	@& "$(PYTHON)" -m streamlit run frontend/app.py

run:
	@if (-not (Test-Path "$(PYTHON)")) { throw "Missing .venv. Create it first: python -m venv .venv" }
	@Start-Process -FilePath "$(PYTHON)" -ArgumentList "-m","backend.main"
	@Start-Process -FilePath "$(PYTHON)" -ArgumentList "-m","streamlit","run","frontend/app.py"
	@Write-Host "Backend started on http://127.0.0.1:5000"
	@Write-Host "Frontend started on http://localhost:8501"

docker-up:
	@docker compose up --build

docker-build:
	@Write-Host "Pulling/updating images from registry..."
	@docker compose pull
	@Write-Host "Done. Use 'make docker-up' to start containers."

docker-down:
	@docker compose down

docker-logs:
	@docker compose logs -f

docker-ps:
	@docker compose ps
