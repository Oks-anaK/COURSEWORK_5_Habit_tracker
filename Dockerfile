FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install --no-cache-dir poetry

# Настройка Poetry
RUN poetry config virtualenvs.create false

# Копирование файлов зависимостей
COPY pyproject.toml ./
COPY poetry.lock* ./

# Установка зависимостей
RUN poetry install --only main --no-root && rm -rf $POETRY_CACHE_DIR

# Копирование проекта
COPY . .

# Создание пользователя для запуска приложения
RUN useradd -m -u 1000 appuser

# Создание папок для статики и медиа с правильными правами
RUN mkdir -p /app/static /app/media && \
    chown -R appuser:appuser /app

# Порт для Gunicorn
EXPOSE 8000

# Переключение на пользователя (после установки всех зависимостей)
USER appuser

# Команда запуска (будет переопределена в docker-compose)
# Используем полный путь к gunicorn или python -m gunicorn
CMD ["python", "-m", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
