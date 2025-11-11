FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only dependency descriptor first for better caching
COPY pyproject.toml ./

# Install runtime dependencies declared in pyproject.toml (FastAPI, Uvicorn)
RUN pip install --no-cache-dir fastapi uvicorn

# Copy application source
COPY . .

# Optional port for FastAPI/Uvicorn
EXPOSE 8000

# Default command runs the project's entrypoint
CMD ["python", "main.py"]