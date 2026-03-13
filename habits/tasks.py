from datetime import datetime, timedelta

from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_reminder


@shared_task
def send_reminder(habit_id):
    """
    Отправка напоминания о конкретной привычке.

    Args:
        habit_id: ID привычки для которой нужно отправить напоминание
    """
    try:
        habit = Habit.objects.get(id=habit_id)
        send_telegram_reminder(habit)
    except Habit.DoesNotExist:
        pass


@shared_task
def send_daily_reminders():
    """
    Отправка ежедневных напоминаний о привычках.
    Проверяет все привычки и отправляет напоминания в нужное время с учетом периодичности.
    """

    from django.utils import timezone

    now = timezone.now()
    current_time = now.time()
    current_date = now.date()

    # Получаем все активные привычки с указанным временем выполнения
    habits = Habit.objects.filter(
        date__isnull=False, user__tg_chat_id__isnull=False
    ).select_related("user")

    for habit in habits:
        if not habit.date:
            continue

        # Конвертируем время привычки в локальное время
        habit_time = timezone.localtime(habit.date).time()

        # Проверяем периодичность - нужно ли выполнять привычку сегодня
        last_execution = habit.executions.order_by("-execution_date").first()

        if last_execution:
            days_since_last = (current_date - last_execution.execution_date).days
            # Если прошло меньше дней, чем периодичность - пропускаем
            if days_since_last < habit.periodicity:
                continue

        # Проверяем, наступило ли время для напоминания (за 5 минут до или в точное время)
        reminder_time = (
            datetime.combine(current_date, habit_time) - timedelta(minutes=5)
        ).time()

        # Отправляем если текущее время между временем напоминания и временем выполнения
        if reminder_time <= current_time <= habit_time:
            result = send_telegram_reminder(habit)
            if result is None:
                print(
                    f"Не удалось отправить напоминание для привычки {habit.id}: нет tg_chat_id"
                )
            elif result.status_code != 200:
                print(f"Ошибка отправки: {result.status_code} - {result.text}")
