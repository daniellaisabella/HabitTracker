# Contributing to Habit Tracker Web Application

Thank you for considering contributing! This guide will help you set up your development environment, run tests, and follow best practices.

## Local Development Setup (.venv)
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Use `uv` for modern dependency management.

## Pre-commit Hooks
Set up pre-commit hooks to enforce code quality before each commit:
```bash
make pre-commit-setup
```
This installs and activates hooks for ruff, pytest, and pyright.

## Linting
Run ruff to check and auto-fix code style:
```bash
make lint
```

## Testing
Run all unit tests with pytest:
```bash
make test
```

## Type Checking
Run static type checks with pyright:
```bash
make typecheck
```

## Deployment (Docker)
1. Build and start services:
   ```bash
   make docker-build
   make docker-up
   ```
2. Stop services:
   ```bash
   make docker-down
   ```

---
For more details, see comments in the Makefile and docker-compose.yml.
