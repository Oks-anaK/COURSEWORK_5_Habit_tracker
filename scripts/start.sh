#!/bin/bash
# Скрипт для запуска проекта одной командой

set -e

echo "🚀 Запуск проекта Habits Tracker..."

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo "📝 Создайте файл .env на основе .env.example"
    exit 1
fi

# Запуск контейнеров
echo "📦 Запуск Docker контейнеров..."
docker compose up -d --build

# Ожидание готовности базы данных
echo "⏳ Ожидание готовности базы данных..."
sleep 5

# Выполнение миграций
echo "🔄 Применение миграций..."
docker compose exec -T web python manage.py migrate

# Сбор статических файлов
echo "📁 Сбор статических файлов..."
docker compose exec -T web python manage.py collectstatic --noinput

echo "✅ Проект успешно запущен!"
echo ""
echo "🌐 Приложение доступно:"
echo "   - API: http://localhost:8080/"
echo "   - Админ-панель: http://localhost:8080/admin/"
echo "   - Документация: http://localhost:8080/swagger/"
echo ""
echo "💡 Для создания суперпользователя выполните:"
echo "   docker compose exec web python manage.py createsuperuser"
