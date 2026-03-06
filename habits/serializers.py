from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения привычек."""

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "date",
            "action",
            "is_pleasant",
            "related_habit",
            "reward",
            "time_to_complete",
            "is_public",
            "periodicity",
        ]
        read_only_fields = ["id", "user"]


class HabitCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления привычек."""

    class Meta:
        model = Habit
        fields = [
            "place",
            "date",
            "action",
            "is_pleasant",
            "related_habit",
            "reward",
            "time_to_complete",
            "is_public",
            "periodicity",
        ]

    def validate(self, attrs):
        """Валидация данных."""
        from .validators import validate_habit_relations

        # Используем существующий экземпляр или создаем новый
        habit = self.instance if self.instance else Habit()
        for key, value in attrs.items():
            setattr(habit, key, value)

        validate_habit_relations(habit)

        return attrs
