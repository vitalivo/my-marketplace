FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь код проекта внутрь образа
COPY . .

# Запуск в продакшн‑режиме (Gunicorn)
CMD ["gunicorn", "payment_service.wsgi:application", "--bind", "0.0.0.0:8000"]