from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, PublicHabitsAPIView

app_name = HabitsConfig.name

router = SimpleRouter()
router.register("", HabitViewSet, basename="habit")

urlpatterns = [
    path("public/", PublicHabitsAPIView.as_view(), name="public_habits"),
]

urlpatterns += router.urls
