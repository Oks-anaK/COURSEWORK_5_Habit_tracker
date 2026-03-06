from django.contrib import admin

from .models import Habit, HabitExecution


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "date", "is_pleasant", "is_public")
    list_filter = ("is_pleasant", "is_public")
    search_fields = ("action", "user__email")


@admin.register(HabitExecution)
class HabitExecutionAdmin(admin.ModelAdmin):
    list_display = ("habit", "execution_date")
    search_fields = ("habit__action",)
