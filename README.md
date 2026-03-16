# Habits Tracker API

API для управления привычками пользователей. Позволяет создавать полезные и приятные привычки, связывать их между собой и отслеживать прогресс.

## Технологии

- **Python 3.12+**
- **Django 6.0+**
- **Django REST Framework**
- **PostgreSQL**
- **Redis**
- **Celery** (асинхронные задачи)
- **JWT** аутентификация
- **Swagger/OpenAPI** документация

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
- `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT` - настройки PostgreSQL
- `LOCATION` - URL Redis (например: `redis://localhost:6379/0`)

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

## API Документация

После запуска сервера документация доступна по адресам:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/

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

## Структура проекта

```
PythonProject14/
├── config/          # Настройки Django
├── habits/          # Приложение привычек
├── users/           # Приложение пользователей
├── manage.py
├── pyproject.toml   # Зависимости Poetry
└── README.md
```

## Автор

Oksana Konkina - oksanka.808@mail.ru

## Лицензия

BSD License
