from django.test import TestCase
from django.contrib.auth import get_user_model
from app.auth.serializers import RegisterSerializer

User = get_user_model()


class RegisterSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }

    def test_create_user(self):
        serializer = RegisterSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_missing_username_fields(self):
        self.data["username"] = ""
        serializer = RegisterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_test_missing_email_fields(self):
        self.data.pop("email")
        serializer = RegisterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
