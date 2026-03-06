from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.user.set_password("testpass123")
        self.user.save()

        self.other_user = User.objects.create(email="other@example.com")
        self.other_user.set_password("testpass123")
        self.other_user.save()
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            action="Выпить стакан воды",
            reward="Съесть мандарин",
            is_public=True,
            periodicity=1,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        """Тест получения списка своих привычек."""
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(data.get("results")[0].get("action"), "Выпить стакан воды")

    def test_habit_retrieve(self):
        """Тест получения конкретной привычки."""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Выпить стакан воды")

    def test_habit_create(self):
        """Тест создания привычки."""
        url = reverse("habits:habit-list")
        data = {
            "place": "На работе",
            "action": "Сделать зарядку",
            "reward": "Выпить кофе",
            "is_public": False,
            "periodicity": 1,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)
        self.assertEqual(Habit.objects.last().user, self.user)

    def test_habit_update(self):
        """Тест обновления привычки."""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {
            "place": "В парке",
            "action": "Пробежать 1 км",
            "reward": "Съесть мандарин",
            "is_public": True,
            "periodicity": 1,
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Пробежать 1 км")

    def test_habit_delete(self):
        """Тест удаления привычки."""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list_other_user(self):
        """Тест: пользователь видит только свои привычки."""
        Habit.objects.create(
            user=self.other_user,
            place="В офисе",
            action="Чужая привычка",
            reward="Награда",
            periodicity=1,
        )

        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(data.get("results")[0].get("action"), "Выпить стакан воды")

    def test_habit_update_other_user(self):
        """Тест: нельзя обновить чужую привычку."""
        other_habit = Habit.objects.create(
            user=self.other_user,
            place="В офисе",
            action="Чужая привычка",
            reward="Награда",
            periodicity=1,
        )

        url = reverse("habits:habit-detail", args=(other_habit.pk,))
        data = {"action": "Измененная привычка"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habits_list(self):
        """Тест получения списка публичных привычек."""
        Habit.objects.create(
            user=self.other_user,
            place="В парке",
            action="Публичная привычка",
            is_public=True,
            periodicity=1,
        )

        url = reverse("habits:public_habits")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(data.get("results")[0].get("action"), "Публичная привычка")
