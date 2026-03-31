# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Копируем requirements и устанавливаем зависимости
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения (без .env)
COPY app/ ./app/

# Создаём директорию для данных
RUN mkdir -p /app/data

# Запускаем приложение
CMD ["python", "app/main.py"]