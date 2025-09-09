# My Marketplace – микросервисная архитектура

## Описание
Проект состоит из двух независимых микросервисов:

| Сервис | Описание |
|--------|----------|
| **auth_service** | Регистрация, аутентификация (JWT), профиль пользователя, health‑endpoint. |
| **marketplace_service** | Категории, товары, CRUD, поиск по радиусу, защищён JWT. |
| **postgres** | PostgreSQL + PostGIS (гео‑данные). |
| **redis** | Кеш/очереди (можно расширять). |

## Как запустить локально

```bash
# Клонировать репозиторий
git clone https://github.com/vitalivo/my-marketplace.git
cd my-marketplace

# Запустить Docker Compose (первый раз построит образы)
docker compose up -d

# Применить миграции (один раз)
docker compose exec auth_service python manage.py migrate
docker compose exec marketplace_service python manage.py migrate
API‑документация
Auth Service – Swagger UI: http://localhost:8000/api/docs/
Marketplace Service – Swagger UI: http://localhost:8001/api/docs/

## Продакшн‑запуск

```bash
# Останавливаем dev‑контейнеры (если они запущены)
docker compose down

# Запускаем в продакшн‑режиме (используем gunicorn)
docker compose -f docker-compose.prod.yml up -d

# Применяем миграции (один раз)
docker compose -f docker-compose.prod.yml exec auth_service python manage.py migrate
docker compose -f docker-compose.prod.yml exec marketplace_service python manage.py migrate

## Payment Service

Сервис отвечает за создание Stripe Checkout‑сессий и хранение информации о платежах.

### Запуск (dev)

```bash
docker compose up -d payment_service
docker compose exec payment_service python manage.py migrate


## Платёжный сервис (payment_service)

### Получить JWT‑токен

```bash
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}' \
  http://localhost:8000/api/token/ | jq -r .access)

echo $TOKEN   # → eyJ...
Создать платёж
curl -X POST http://localhost:8002/api/payments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount":12.50,"currency":"usd","success_url":"https://example.com/success/","cancel_url":"https://example.com/cancel/"}' | jq