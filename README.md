# agentic-saas-backend

Small backend prototype for managing agents and tenants.

## Overview

-   Entrypoint: `src/main.py` — program entry.
-   Config: `src/database/core.py` reads DB values from `.env`.
-   Data models: `src/entities/agent.py` and `src/entities/tenant.py`.
-   Rate limiter and custom exceptions live under `src/`.

## Requirements

See runtime dependencies in `pyproject.toml`.

## Local Setup
```bash
# 1. Clone and enter project directory
git clone https://github.com/siddharth794/agentic-saas-backend.git
cd agentic-saas-backend

# 2. Switch to develop branch
git checkout develop

# 3. Create .env file from example (macOS/Linux)
cp .env.example .env
# For Windows use: 
copy .env.example .env

# 4. Create database in MySQL (ensure the name matches .env DB_NAME)

# 5. Create virtual environment and install all dependencies
uv sync

# 6. Apply migrations
alembic upgrade head
```

## For Migrations


## Quickstart (Docker)

Build and run with Docker Compose:

```bash
docker-compose up --build
```

Alternatively build and run the image directly:

```bash
docker build -t agentic-saas-backend:latest .
docker run --rm -p 8000:8000 -e PYTHONPATH=/app agentic-saas-backend:latest
```

The project Dockerfile runs `python src/main.py` and docker-compose maps host port 8000 -> container 8000 by default.

## Environment

Copy `.env.example` to `.env` and populate DB and other settings used by `src/database/core.py`.

## Project layout

-   src/
    -   main.py — program entry
    -   rate_limiter.py
    -   exceptions.py
    -   database/
        -   core.py — settings and engine
    -   entities/
        -   agent.py
        -   tenant.py

## Development notes

-   Python runtime/version is declared in `pyproject.toml` / `.python-version`.
-   Dependencies managed via `pyproject.toml`.
-   Replace `src/main.py` with an ASGI server (uvicorn) if exposing HTTP APIs.

## 🧩 Contributing Workflow
First fork the repo in your github
```bash
# 1. Clone and enter project directory
git clone https://github.com/siddharth794/agentic-saas-backend.git
cd agentic-saas-backend

# 2. Make sure you're on the develop branch
git checkout develop

# 3. Pull the latest changes
git pull origin develop

# 4. Create a new feature branch from develop
# Replace FEATURE_NAME with your task/feature name
git checkout -b feature/FEATURE_NAME

# 5. Work on your changes...
# (edit code, commit, etc.)

# 6. Stage and commit your changes
git add .
git commit -m "feat: describe your feature"

# 7. Push your branch to the remote repository
git push -u origin feature/FEATURE_NAME

# 8. Create a Pull Request (PR) into the 'develop' branch on upstream(not your forked one but this repo develop branch)


## License

Add a license file to this repository as needed.
