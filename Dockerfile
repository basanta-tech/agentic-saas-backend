FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential wget curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv
RUN pip install alembic

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install deps
RUN uv sync --frozen --no-dev

# Copy project (but NOT overwriting .venv)
COPY . .

RUN .venv/bin/alembic  upgrade head

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
