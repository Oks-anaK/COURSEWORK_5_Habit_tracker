from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com", town="Москва")
        self.user.set_password("testpass123")
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """Тест регистрации пользователя."""
        initial_count = User.objects.count()
        url = reverse("users:register")
        data = {
            "email": "test@email.ru",
            "password": "testpass456",
            "password1": "testpass456",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), initial_count + 1)
        self.assertTrue(User.objects.filter(email="test@email.ru").exists())

    def test_user_update(self):
        """Тест обновления профиля пользователя."""
        url = reverse("users:user_update", args=(self.user.pk,))
        data = {
            "first_name": "Ирина",
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Ирина")

    def test_user_retrieve(self):
        """Тест просмотра профиля пользователя."""
        url = reverse("users:user_detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("town"), "Москва")

    def test_user_delete(self):
        """Тест удаления пользователя."""
        url = reverse("users:user_destroy", args=(self.user.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
