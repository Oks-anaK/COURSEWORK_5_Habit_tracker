import os
import sys

import django

from habits.models import Habit
from habits.services import send_telegram_reminder

# Установка кодировки вывода для поддержки эмодзи
sys.stdout.reconfigure(encoding="utf-8")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Найти привычку с заполненным tg_chat_id
habit = Habit.objects.filter(user__tg_chat_id__isnull=False).first()

if not habit:
    print("Ошибка: Не найдена привычка с заполненным tg_chat_id")
    print("Проверьте в админке, что у пользователя указан 'Телеграм chat-id'")
else:
    print(f"Привычка: {habit.action}")
    print(f"Пользователь: {habit.user.email}")
    print(f"Chat ID: {habit.user.tg_chat_id}")
    print("\nОтправляю сообщение...")

    result = send_telegram_reminder(habit)

    if result is None:
        print("Ошибка: Не удалось отправить (нет tg_chat_id или другая проблема)")
    elif result.status_code == 200:
        print("OK: Сообщение успешно отправлено в Telegram!")
        print(f"Ответ: {result.json()}")
    else:
        print(f"Ошибка отправки: {result.status_code}")
        print(f"Ответ: {result.text}")
