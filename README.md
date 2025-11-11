# agentic-saas-backend

Small backend prototype for managing agents and tenants.

## Overview

-   Entrypoint: `src/main.py` — program entry.
-   Config: `src/database/core.py` reads DB values from `.env`.
-   Data models: `src/entities/agent.py` and `src/entities/tenant.py`.
-   Rate limiter and custom exceptions live under `src/`.

## Requirements

See runtime dependencies in `pyproject.toml`.

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

## License

Add a license file to this repository as needed.
