from django.core.exceptions import ValidationError


def validate_time_to_complete(value):
    """
    Валидатор для времени выполнения привычки.
    Время выполнения должно быть не больше 120 секунд.
    """
    if value is not None and value > 120:
        raise ValidationError(
            "Время выполнения должно быть не больше 120 секунд."
        )


def validate_periodicity(value):
    """
    Валидатор для периодичности выполнения привычки.
    Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    """
    if value is not None and value > 7:
        raise ValidationError(
            "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
        )


def validate_habit_execution_frequency(habit):
    """
    Валидация частоты выполнения привычки.
    Проверяет, что привычка выполняется хотя бы раз в 7 дней.
    """
    from datetime import date, timedelta
    
    if habit.pk:  # Проверяем только для существующих привычек
        # Получаем последнее выполнение привычки
        last_execution = habit.executions.order_by('-execution_date').first()
        
        if last_execution:
            days_since_last = (date.today() - last_execution.execution_date).days
            if days_since_last > 7:
                raise ValidationError(
                    f"Нельзя не выполнять привычку более 7 дней. "
                    f"Последнее выполнение было {days_since_last} дней назад."
                )


def validate_habit_relations(habit):
    """
    Валидация связей между полезными и приятными привычками.
    
    Правила:
    - Для полезных привычек должна быть либо связанная привычка, либо награда
    - Связанная привычка должна быть приятной
    - Приятные привычки не могут иметь связанную привычку или награду
    """
    if not habit.is_pleasant:  # Для полезных привычек

        if not habit.related_habit and not habit.reward:
            raise ValidationError(
                "Для полезной привычки необходимо указать либо связанную привычку, либо награду"
            )

        if habit.related_habit and habit.reward:
            raise ValidationError(
                "Нельзя одновременно указывать связанную привычку и награду"
            )

        if habit.related_habit and not habit.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")

    else:  # Для приятных привычек

        if habit.related_habit:
            raise ValidationError("Приятная привычка не может иметь связанную привычку")

        if habit.reward:
            raise ValidationError("Приятная привычка не должна иметь награду")
