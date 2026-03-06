from django.core.validators import MinValueValidator
from django.db import models

from habits.validators import (validate_habit_execution_frequency,
                               validate_habit_relations, validate_periodicity,
                               validate_time_to_complete)
from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Добавьте создателя привычки.",
        related_name="hab_user",
    )
    place = models.CharField(
        max_length=200,
        verbose_name="Место выполнения",
        help_text="Укажите место, в котором необходимо выполнять привычку.",
    )
    date = models.DateTimeField(
        verbose_name="Время выполнения",
        help_text="Укажите время, когда необходимо выполнять привычку.",
        null=True,
        blank=True,
    )
    action = models.CharField(
        max_length=500,
        verbose_name="Действие",
        help_text="Выберите действие, которое представляет собой привычка.",
    )
    # ПРИЗНАК ПРИЯТНОЙ ПРИВЫЧКИ
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Признак приятной привычки - можно привязать к выполнению полезной привычки",
    )
    # СВЯЗАННАЯ ПРИВЫЧКА
    related_habit = models.ForeignKey(
        "self",  # Ссылка на саму модель Habit
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_habits",
        verbose_name="Связанная привычка",
        help_text="Связанная привычка (указывается для полезных привычек, не для приятных)",
        limit_choices_to={"is_pleasant": True},
    )
    # Альтернатива связанной привычке
    reward = models.CharField(max_length=200, blank=True, verbose_name="Вознаграждение")
    time_to_complete = models.PositiveIntegerField(
        verbose_name="Время выполнения (в секундах)",
        help_text=(
            "Укажите время в секундах, которое предположительно потратит пользователь"
            "на выполнение привычки (не более 120 секунд)."
        ),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), validate_time_to_complete],
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
        help_text="Интервал между выполнениями привычки в днях (не более 7 дней).",
        validators=[MinValueValidator(1), validate_periodicity],
    )

    def clean(self):
        """Валидация бизнес-логики"""
        validate_habit_relations(self)
        validate_habit_execution_frequency(self)

    def __str__(self):
        return f"{self.action} ({self.user.email if self.user else 'Без пользователя'})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"


class HabitExecution(models.Model):
    """
    Модель для отслеживания выполнения привычек.
    Позволяет проверять, что привычка выполняется хотя бы раз в 7 дней.
    """

    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="executions",
        verbose_name="Привычка",
    )
    execution_date = models.DateField(
        verbose_name="Дата выполнения",
        auto_now_add=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Время создания записи",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Выполнение привычки"
        verbose_name_plural = "Выполнения привычек"
        ordering = ["-execution_date"]

    def __str__(self):
        return f"{self.habit.action} - {self.execution_date}"
