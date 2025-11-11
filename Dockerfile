# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv (modern dependency manager)
RUN pip install --no-cache-dir uv

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy rest of the source code
COPY . .

# Environment setup
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the app
CMD ["python", "src/main.py"]
