# --------------------------------------------------------------
#  Dockerfile –  python 3.13 slim + все dev‑зависимости
# --------------------------------------------------------------
FROM python:3.13-slim

# ---------- Системные зависимости ----------
#   build-essential  → gcc + libc6-dev (нужен assert.h и др.)
#   python3.13-dev   → заголовки CPython 3.13 (Python.h, _PyInterpreterState_Get)
#   libpq-dev        → заголовки PostgreSQL (для psycopg2)
#   libffi-dev       → требуется cffi/psycopg2
#   libssl-dev       → иногда требуется для cryptography‑зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3.13-dev \
        libpq-dev \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# ---------- Рабочая директория ----------
WORKDIR /app

# ---------- entrypoint ----------
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# ---------- Копируем код проекта ----------
COPY . /app

# ---------- Python‑зависимости ----------
#   --no-cache-dir – не сохраняем промежуточный кэш в образ
RUN pip install --no-cache-dir -r requirements.txt