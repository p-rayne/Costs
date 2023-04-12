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
            "password2": "testpassword",
        }

    def test_validate_password(self):
        serializer = RegisterSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        self.data["password"] = "weak"
        self.data["password2"] = "weak"
        serializer = RegisterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_create_user(self):
        serializer = RegisterSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_missing_fields(self):
        self.data["username"] = ""
        serializer = RegisterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_fields_are_required(self):
        self.data.pop("email")
        serializer = RegisterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
