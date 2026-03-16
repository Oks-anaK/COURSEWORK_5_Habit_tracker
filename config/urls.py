from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Habits API",
        default_version="v1",
        description="""
API для управления привычками пользователей.

**Основные возможности:**
- Создание, просмотр, обновление и удаление привычек
- Разделение на полезные и приятные привычки
- Связывание привычек (полезная + приятная награда)
- Установка периодичности выполнения (1-7 дней)
- Просмотр публичных привычек других пользователей

**Аутентификация:**
Для доступа к защищенным эндпоинтам необходимо зарегистрироваться через `/users/register/`,
получить JWT токены через `/users/login/` и использовать access токен в заголовке:
`Authorization: Bearer <token>`

**Правила:**
- Полезная привычка должна иметь либо связанную приятную привычку, либо вознаграждение
- Время выполнения: от 1 до 120 секунд
- Периодичность: от 1 до 7 дней
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@habits.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("habits/", include("habits.urls", namespace="habits")),
    path("users/", include("users.urls", namespace="users")),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
