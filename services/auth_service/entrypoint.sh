#!/bin/sh
set -e

# Ждём готовности PostgreSQL
echo "Waiting for PostgreSQL..."
until pg_isready -h "${POSTGRES_HOST:-postgres}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-dev}" >/dev/null 2>&1; do
  sleep 1
done

# Применяем миграции Django (если они нужны)
echo "Running migrations..."
python manage.py migrate --noinput

# Запускаем команду, переданную через `docker compose command:`
exec "$@"
chmod +x services/*/entrypoint.sh