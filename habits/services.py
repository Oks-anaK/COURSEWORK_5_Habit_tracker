import requests
from django.conf import settings
from django.utils import timezone


def send_telegram_message(chat_id, message):
    """Отправка текстового сообщения в конкретный чат Telegram."""
    url = f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage'
    
    data = {
        'chat_id': chat_id,
        'text': message,
    }
    
    response = requests.get(url=url, data=data)
    return response


def send_telegram_reminder(habit):
    """Отправка напоминания о привычке в Telegram."""

    if not habit.user or not habit.user.tg_chat_id:
        return None

    message_parts = [
        f"🔔 Напоминание о привычке!",
        f"",
        f"Действие: {habit.action}",
        f"Место: {habit.place}",
    ]
    
    # Добавляем время выполнения, если указано
    if habit.date:
        local_time = timezone.localtime(habit.date)
        message_parts.append(f"Время: {local_time.strftime('%H:%M')}")
    
    # Добавляем время на выполнение
    if habit.time_to_complete:
        message_parts.append(f"Время выполнения: {habit.time_to_complete} секунд")
    
    # Добавляем награду или связанную привычку
    if habit.reward:
        message_parts.append(f"Вознаграждение: {habit.reward}")
    elif habit.related_habit:
        message_parts.append(f"Связанная привычка: {habit.related_habit.action}")
    
    message = "\n".join(message_parts)
    
    return send_telegram_message(habit.user.tg_chat_id, message)
