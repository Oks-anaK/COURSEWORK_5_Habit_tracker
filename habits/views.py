from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Habit
from .paginators import CustomPagination
from .serializers import HabitCreateSerializer, HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD операции для привычек текущего пользователя."""

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_permissions(self):
        """Возвращает список разрешений для данного действия."""
        if self.action in ["update", "partial_update", "destroy"]:
            from users.permissions import IsOwnerOrReadOnly

            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Возвращает только привычки текущего пользователя."""
        return Habit.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action in ["create", "update", "partial_update"]:
            return HabitCreateSerializer
        return HabitSerializer

    def perform_create(self, serializer):
        """Привязывает привычку к текущему пользователю."""
        habit = serializer.save(user=self.request.user)
        habit.full_clean()
        habit.save()

    def perform_update(self, serializer):
        """Обновляет привычку с валидацией."""
        habit = serializer.save()
        habit.full_clean()
        habit.save()


class PublicHabitsAPIView(APIView):
    """Список публичных привычек (только чтение)."""

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        """Возвращает список публичных привычек с пагинацией."""
        public_habits = Habit.objects.filter(is_public=True)

        paginator = CustomPagination()
        paginated_habits = paginator.paginate_queryset(public_habits, request)
        serializer = HabitSerializer(paginated_habits, many=True)

        return paginator.get_paginated_response(serializer.data)
