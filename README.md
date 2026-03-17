# Habits Tracker API

API для управления привычками пользователей. Позволяет создавать полезные и приятные привычки, связывать их между собой и отслеживать прогресс.

## Технологии

- **Python 3.12+**
- **Django 6.0+**
- **Django REST Framework**
- **PostgreSQL 15**
- **Redis**
- **Celery** (асинхронные задачи)
- **JWT** аутентификация
- **Swagger/OpenAPI** документация
- **Docker & Docker Compose** (контейнеризация)
- **Nginx** (веб-сервер)
- **Gunicorn** (WSGI-сервер)

## Функциональность

- ✅ CRUD операции для привычек
- ✅ Разделение на полезные и приятные привычки
- ✅ Связывание привычек (полезная + приятная награда)
- ✅ Установка периодичности выполнения (1-7 дней)
- ✅ Просмотр публичных привычек других пользователей
- ✅ JWT аутентификация
- ✅ Автоматические напоминания через Celery
- ✅ Пагинация результатов
- ✅ Валидация бизнес-логики

## Установка

### Требования

- Python 3.12+
- PostgreSQL
- Redis
- Poetry (для управления зависимостями)

### Шаги установки

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd PythonProject14
```

2. Установите зависимости:
```bash
poetry install
```

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Заполните переменные окружения в `.env`:
- `SECRET_KEY` - секретный ключ Django
- `DEBUG` - режим отладки (True/False)
- `ALLOWED_HOSTS` - разрешённые хосты (через запятую)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` - настройки PostgreSQL
- `CELERY_BROKER_URL` - URL Redis для Celery (например: `redis://localhost:6379/0`)
- `CELERY_RESULT_BACKEND` - URL Redis для результатов Celery
- `TELEGRAM_BOT_TOKEN` - токен Telegram-бота для напоминаний

5. Примените миграции:
```bash
poetry run python manage.py migrate
```

6. Создайте суперпользователя (опционально):
```bash
poetry run python manage.py createsuperuser
```

## Запуск

### Запуск сервера разработки

```bash
poetry run python manage.py runserver
```

### Запуск Celery worker

В отдельном терминале:
```bash
poetry run celery -A config worker -l info
```

### Запуск Celery beat (для периодических задач)

В отдельном терминале:
```bash
poetry run celery -A config beat -l info
```

## Запуск с Docker

### Требования

- Docker и Docker Compose

### Быстрый старт

1. **Создайте файл `.env`** (см. раздел "Установка")

2. **Запустите все сервисы:**
```bash
docker compose up -d --build
```

3. **Выполните миграции:**
```bash
docker compose exec web python manage.py migrate
```

4. **Соберите статические файлы:**
```bash
docker compose exec web python manage.py collectstatic --noinput
```

5. **Создайте суперпользователя:**
```bash
docker compose exec web python manage.py createsuperuser
```

6. **Приложение доступно:**
- API: http://localhost:8080/
- Админ-панель: http://localhost:8080/admin/
- Документация: http://localhost:8080/swagger/

### Управление контейнерами

```bash
# Просмотр статуса
docker compose ps

# Просмотр логов
docker compose logs -f web
docker compose logs -f celery

# Остановка
docker compose down

# Пересборка образов
docker compose up -d --build
```

## Деплой на сервер

### Подготовка сервера

1. **Подключитесь к серверу:**
```bash
ssh deploy@SERVER_IP
# Для данного проекта: ssh deploy@158.160.230.124
```

2. **Клонируйте репозиторий:**
```bash
cd ~/apps
git clone <repository-url> COURSEWORK_5_Habit_tracker
cd COURSEWORK_5_Habit_tracker
```

3. **Создайте `.env` файл для продакшена:**
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-server-ip,domain.com

DB_NAME=habits_db
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432

# Redis и Celery настройки (для Docker LOCATION=redis://redis:6379/0)
LOCATION=my_location

TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

4. **Запустите приложение:**
```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

5. **Приложение будет доступно на порту 8080**

### Обновление на сервере

```bash
cd ~/apps/COURSEWORK_5_Habit_tracker
git pull
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose restart web celery celery-beat
```

## 🌐 Развернутое приложение

**Адрес сервера:** http://158.160.230.124:8080/

- **API**: http://158.160.230.124:8080/
- **Админ-панель**: http://158.160.230.124:8080/admin/
- **Документация API (Swagger)**: http://158.160.230.124:8080/swagger/

## API Документация

После запуска сервера документация доступна по адресам:

**Локальная разработка:**
- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/

**Docker/Продакшен:**
- **Swagger UI**: http://localhost:8080/swagger/ (или ваш домен)
- **ReDoc**: http://localhost:8080/redoc/

## Использование API

### Регистрация и аутентификация

1. Зарегистрируйтесь: `POST /users/register/`
2. Получите токены: `POST /users/login/`
3. Используйте токен в заголовке: `Authorization: Bearer <access_token>`

### Примеры запросов

**Создание полезной привычки:**
```json
POST /habits/
{
  "place": "Дом",
  "action": "Выпить стакан воды",
  "time_to_complete": 30,
  "periodicity": 1,
  "reward": "Посмотреть сериал"
}
```

**Создание приятной привычки:**
```json
POST /habits/
{
  "place": "Диван",
  "action": "Посмотреть сериал",
  "is_pleasant": true,
  "periodicity": 1
}
```

**Связывание привычек:**
```json
POST /habits/
{
  "place": "Дом",
  "action": "Выпить стакан воды",
  "time_to_complete": 30,
  "periodicity": 1,
  "related_habit": 2
}
```

## Правила валидации

- Полезная привычка должна иметь либо связанную приятную привычку, либо вознаграждение
- Время выполнения: от 1 до 120 секунд
- Периодичность: от 1 до 7 дней
- Приятная привычка не может иметь связанную привычку или вознаграждение

## Тестирование

Запуск тестов:
```bash
poetry run python manage.py test
```

Проверка покрытия кода:
```bash
poetry run coverage run --source='.' manage.py test
poetry run coverage report
```

## Линтинг и форматирование

Проверка кода:
```bash
poetry run flake8 .
```

Форматирование кода:
```bash
poetry run black .
poetry run isort .
```

## CI/CD

Проект использует GitHub Actions для автоматизации тестирования, линтинга и деплоя.

### Этапы CI/CD Pipeline

1. **Тестирование** (`test` job):
   - Установка зависимостей через Poetry
   - Запуск линтера (flake8, black)
   - Запуск тестов Django

2. **Проверка Docker** (`docker-build` job):
   - Валидация docker-compose.yml
   - Сборка Docker-образа
   - Проверка синтаксиса Docker Compose

3. **Деплой** (`deploy` job):
   - Автоматический деплой на сервер при пуше в `main`, `master` или `develop`
   - Обновление кода через `git pull`
   - Пересборка и перезапуск контейнеров
   - Применение миграций
   - Сбор статических файлов

### Настройка CI/CD

Для работы деплоя необходимо настроить GitHub Secrets:
- `SSH_HOST` - IP адрес сервера
- `SSH_USER` - пользователь для SSH (обычно `deploy`)
- `SSH_PRIVATE_KEY` - приватный SSH ключ
- `SSH_PORT` - порт SSH (опционально, по умолчанию 22)

Workflow файл: `.github/workflows/ci-cd.yml`

## Структура проекта

```
PythonProject14/
├── config/              # Настройки Django
├── habits/              # Приложение привычек
├── users/               # Приложение пользователей
├── nginx/               # Конфигурация Nginx
│   ├── Dockerfile
│   └── nginx.conf
├── manage.py
├── pyproject.toml        # Зависимости Poetry
├── Dockerfile           # Образ приложения
├── docker-compose.yml   # Docker Compose конфигурация
├── .env                 # Переменные окружения (не в git)
└── README.md
```

## Автор

Oksana Konkina - oksanka.808@mail.ru

## Лицензия

BSD License
