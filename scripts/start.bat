@echo off
REM Скрипт для запуска проекта одной командой (Windows)

echo 🚀 Запуск проекта Habits Tracker...

REM Проверка наличия .env файла
if not exist .env (
    echo ⚠️  Файл .env не найден!
    echo 📝 Создайте файл .env на основе .env.example
    exit /b 1
)

REM Запуск контейнеров
echo 📦 Запуск Docker контейнеров...
docker compose up -d --build

REM Ожидание готовности базы данных
echo ⏳ Ожидание готовности базы данных...
timeout /t 5 /nobreak >nul

REM Выполнение миграций
echo 🔄 Применение миграций...
docker compose exec -T web python manage.py migrate

REM Сбор статических файлов
echo 📁 Сбор статических файлов...
docker compose exec -T web python manage.py collectstatic --noinput

echo ✅ Проект успешно запущен!
echo.
echo 🌐 Приложение доступно:
echo    - API: http://localhost:8080/
echo    - Админ-панель: http://localhost:8080/admin/
echo    - Документация: http://localhost:8080/swagger/
echo.
echo 💡 Для создания суперпользователя выполните:
echo    docker compose exec web python manage.py createsuperuser
