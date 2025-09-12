#!/bin/sh
set -e

echo "=== Notification Service entrypoint ==="

# Немного ждём, чтобы PostgreSQL успел подняться (можно убрать, если не нужно)
echo "Giving PostgreSQL a few seconds to start..."
sleep 5

echo "Waiting for PostgreSQL ($POSTGRES_HOST:$POSTGRES_PORT) as $POSTGRES_USER ..."
until pg_isready -h "${POSTGRES_HOST:-postgres}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-dev}" >/dev/null 2>&1; do
  echo "Postgres not ready yet – retry in 1s"
  sleep 1
done

echo "PostgreSQL is ready – running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec "$@"