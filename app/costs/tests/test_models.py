from django.test import TestCase
from django.contrib.auth.models import User
from app.costs.models import Category, Cost
from datetime import date


class CategoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )

    def test_category_creation(self):
        category = Category.objects.create(
            owner=self.user, name="TestCategory", description="TestDescription"
        )
        self.assertEqual(category.owner, self.user)
        self.assertEqual(category.name, "TestCategory")
        self.assertEqual(category.description, "TestDescription")


class CostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.category = Category.objects.create(
            owner=self.user, name="TestCategory", description="TestDescription"
        )

    def test_cost_creation(self):
        cost = Cost.objects.create(
            owner=self.user, category=self.category, value=100.0, date=date.today()
        )
        self.assertEqual(cost.owner, self.user)
        self.assertEqual(cost.category, self.category)
        self.assertEqual(cost.value, 100.0)
        self.assertEqual(cost.date, date.today())

    def test_default_category_creation(self):
        self.assertEqual(Category.objects.filter(owner=self.user).count(), 4 + 1)
