from django.urls import path
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import (DecoratedTokenObtainPairView,
                         DecoratedTokenRefreshView, UserCreateAPIView,
                         UserDestroyAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        DecoratedTokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        DecoratedTokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("<int:pk>/destroy/", UserDestroyAPIView.as_view(), name="user_destroy"),
]
