from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from app.costs.models import Category
from app.costs.serializers import CategorySerializer, CostSerializer


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.category_data = {
            "name": "test_category",
            "description": "test_description",
        }
        self.request = self.factory.get("/api/v1/category/")
        self.request.user = self.user

    def test_category_creation(self):
        category_serializer = CategorySerializer(
            data=self.category_data, context={"request": self.request}
        )
        self.assertTrue(category_serializer.is_valid())
        category = category_serializer.save()
        self.assertEqual(category.name, self.category_data["name"])
        self.assertEqual(category.description, self.category_data["description"])
        self.assertEqual(category.owner, self.user)

    def test_category_uniqueness(self):
        Category.objects.create(owner=self.user, **self.category_data)
        category_serializer = CategorySerializer(
            data=self.category_data, context={"request": self.request}
        )
        self.assertFalse(category_serializer.is_valid())
        self.assertIn("non_field_errors", category_serializer.errors)


class CostSerializerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.category = Category.objects.create(name="test_category", owner=self.user)
        self.cost_data = {
            "category": self.category.id,
            "value": 100,
            "date": "2022-01-01",
            "note": "test_note",
        }
        self.request = self.factory.get("/api/v1/cost/")
        self.request.user = self.user

    def test_cost_creation(self):
        cost_serializer = CostSerializer(
            data=self.cost_data, context={"request": self.request}
        )
        self.assertTrue(cost_serializer.is_valid())
        cost = cost_serializer.save()
        self.assertEqual(cost.category, self.category)
        self.assertEqual(cost.value, self.cost_data["value"])
        self.assertEqual(cost.date.strftime("%Y-%m-%d"), self.cost_data["date"])
        self.assertEqual(cost.note, self.cost_data["note"])

    def test_cost_value_validation(self):
        self.cost_data["value"] = -1
        cost_serializer = CostSerializer(
            data=self.cost_data, context={"request": self.request}
        )
        self.assertFalse(cost_serializer.is_valid())
        self.assertIn("value", cost_serializer.errors)

    def test_create_not_belong_category(self):
        user_2 = User.objects.create_user(
            username="test_user_2", password="test_password"
        )
        category = Category.objects.create(name="test_category_2", owner=user_2)
        self.cost_data["category"] = category.id

        cost_serializer = CostSerializer(
            data=self.cost_data, context={"request": self.request}
        )
        self.assertFalse(cost_serializer.is_valid())
        self.assertEqual(
            cost_serializer.errors["category"][0],
            "This category does not belong to this user.",
        )
