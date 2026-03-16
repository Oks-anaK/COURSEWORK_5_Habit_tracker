from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        operation_summary="Получить список привычек пользователя",
        operation_description="Возвращает только привычки текущего пользователя с пагинацией",
        tags=["Привычки"],
    )
    def list(self, request, *args, **kwargs):
        """Получить список привычек пользователя."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить детали привычки",
        operation_description="Возвращает детальную информацию о конкретной привычке",
        tags=["Привычки"],
    )
    def retrieve(self, request, *args, **kwargs):
        """Получить детали привычки."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новую привычку",
        operation_description="Создает новую привычку для текущего пользователя",
        tags=["Привычки"],
    )
    def create(self, request, *args, **kwargs):
        """Создать новую привычку."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить привычку",
        operation_description="Полное обновление привычки (только владелец)",
        tags=["Привычки"],
    )
    def update(self, request, *args, **kwargs):
        """Обновить привычку."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить привычку",
        operation_description="Частичное обновление привычки (только владелец)",
        tags=["Привычки"],
    )
    def partial_update(self, request, *args, **kwargs):
        """Частично обновить привычку."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить привычку",
        operation_description="Удаляет привычку (только владелец)",
        tags=["Привычки"],
    )
    def destroy(self, request, *args, **kwargs):
        """Удалить привычку."""
        return super().destroy(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="Получить список публичных привычек",
        operation_description="Возвращает список публичных привычек всех пользователей с пагинацией",
        tags=["Привычки"],
    )
    def get(self, request):
        """Возвращает список публичных привычек с пагинацией."""
        public_habits = Habit.objects.filter(is_public=True)

        paginator = CustomPagination()
        paginated_habits = paginator.paginate_queryset(public_habits, request)
        serializer = HabitSerializer(paginated_habits, many=True)

        return paginator.get_paginated_response(serializer.data)
