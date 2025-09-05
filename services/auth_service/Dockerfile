# ---- Base image ----
FROM python:3.11-slim

# ---- Install system build deps (only for psycopg2) ----
#   - libpq-dev   → pg_config (PostgreSQL client headers)
#   - gcc, python3-dev → компилятор для C‑расширений
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ---- Working directory ----
WORKDIR /app

# ---- Install python deps ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Clean up build‑time deps (optional, makes image smaller) ----
RUN apt-get purge -y --auto-remove gcc libpq-dev && \
    rm -rf /root/.cache/pip

# ---- Copy project source ----
COPY . .

# ---- Run server ----
CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000"]