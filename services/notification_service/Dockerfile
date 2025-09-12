FROM python:3.13-slim

# Установим системные зависимости (включая клиент PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3.13-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . /app

# Устанавливаем Python‑зависимости
RUN pip install --no-cache-dir -r requirements.txt

# По умолчанию entrypoint будет вызываться, а CMD – это команда gunicorn
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "notification_service.wsgi:application", "--bind", "0.0.0.0:8003"]