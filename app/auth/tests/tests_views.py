from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class RegisterViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("auth_register")
        self.data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, self.data["username"])

    def test_register_user_with_weak_password(self):
        self.data["password"] = "weak"
        response = self.client.post(self.register_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn("password", response.data)

    def test_register_user_with_missing_fields(self):
        self.data["username"] = ""
        response = self.client.post(self.register_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn("username", response.data)

    def test_register_user_with_existing_email(self):
        User.objects.create_user(
            username="testuser2", email="testuser@example.com", password="testpassword"
        )
        response = self.client.post(self.register_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertIn("email", response.data)
