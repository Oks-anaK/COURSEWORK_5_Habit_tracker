from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.models import User
from users.permissions import IsUserOwner
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Регистрация нового пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Создать профиль",
        operation_description="Создает профиль для пользователя",
        tags=["Пользователи"],
    )
    def post(self, request, *args, **kwargs):
        """Создать профиль."""
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Создает пользователя с хешированным паролем."""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    """Получение информации о пользователе."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)

    @swagger_auto_schema(
        operation_summary="Посмотреть профиль",
        operation_description="Посмотреть профиль текущего пользователя",
        tags=["Пользователи"],
    )
    def get(self, request, *args, **kwargs):
        """Посмотреть профиль."""
        return super().retrieve(request, *args, **kwargs)


class UserUpdateAPIView(UpdateAPIView):
    """Обновление информации о пользователе."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)

    @swagger_auto_schema(
        operation_summary="Изменить профиль (PUT)",
        operation_description="Полное обновление профиля текущего пользователя",
        tags=["Пользователи"],
    )
    def put(self, request, *args, **kwargs):
        """Изменить профиль (PUT)."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Изменить профиль (PATCH)",
        operation_description="Частичное обновление профиля текущего пользователя",
        tags=["Пользователи"],
    )
    def patch(self, request, *args, **kwargs):
        """Изменить профиль (PATCH)."""
        return super().partial_update(request, *args, **kwargs)


class UserDestroyAPIView(DestroyAPIView):
    """Удаление пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)

    @swagger_auto_schema(
        operation_summary="Удалить профиль",
        operation_description="Удалить профиль текущего пользователя",
        tags=["Пользователи"],
    )
    def delete(self, request, *args, **kwargs):
        """Удалить профиль."""
        return super().destroy(request, *args, **kwargs)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    """Вход в систему с получением JWT токенов."""

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Войти в систему",
        operation_description="Получить JWT токены (access и refresh) для аутентификации. Требует email и password.",
        tags=["Пользователи"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    """Обновление access токена."""

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Обновить токен",
        operation_description="Обновить access токен используя refresh токен. Возвращает новый access токен.",
        tags=["Пользователи"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
