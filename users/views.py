from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsUserOwner
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Регистрация нового пользователя."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

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


class UserUpdateAPIView(UpdateAPIView):
    """Обновление информации о пользователе."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)


class UserDestroyAPIView(DestroyAPIView):
    """Удаление пользователя."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)
