# Multi-stage Dockerfile to produce a smaller runtime image
# Builder stage: install dependencies
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc libpq-dev && \
    python -m pip install --upgrade pip && \
    python -m pip install --prefix=/install -r requirements.txt && \
    apt-get remove -y build-essential gcc libpq-dev && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Final stage: copy installed packages and app code
FROM python:3.11-slim as runtime

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Copy installed packages from build stage
COPY --from=builder /install /usr/local

# Copy app sources
COPY . /app

# Ensure static dir exists so startup doesn't fail
RUN mkdir -p /app/static

# Copy gunicorn config
COPY gunicorn.conf.py /app/gunicorn.conf.py

# Expose default port
EXPOSE 8000

# Run as non-root
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser || true
USER appuser

# Entrypoint: gunicorn with config
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app.main:app"]
