# import datetime
# from django.db.models import Sum, F
# from django.urls import reverse
# from django.test import TestCase
# from rest_framework import status
# from rest_framework.test import APIClient
# from app.costs.models import Category, Cost
# from app.costs.serializers import CategorySerializer, CostSerializer
# from django.contrib.auth import get_user_model

# USER = get_user_model()


# class CostTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = USER.objects.create_user(
#             email="test@gmail.com", password="testpassword", username="testuser"
#         )
#         self.category_1 = Category.objects.create(
#             name="test_category_1", owner=self.user
#         )
#         self.cost = Cost.objects.create(
#             value=100,
#             date=datetime.date.today(),
#             owner=self.user,
#             category=self.category_1,
#         )
#         self.client.force_authenticate(user=self.user)

#     def test_list_costs(self):
#         res = self.client.get(reverse("cost-list"))
#         costs = (
#             Cost.objects.all()
#             .order_by("-date")
#             .annotate(category_name=F("category__name"))
#         )
#         serializer = CostSerializer(costs, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)

#     def test_create_cost_successful(self):
#         payload = {
#             "value": 200,
#             "date": datetime.date.today().strftime("%Y-%m-%d"),
#             "category": self.category_1.id,
#         }
#         res = self.client.post(reverse("cost-list"), payload)
#         exists = Cost.objects.filter(
#             owner=self.user,
#             value=payload["value"],
#             category=payload["category"],
#             date=payload["date"],
#         ).exists()
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(exists)

#     def test_create_cost_with_invalid_category(self):
#         payload = {
#             "value": 200,
#             "date": datetime.date.today().strftime("%Y-%m-%d"),
#             "category": 99,
#         }
#         res = self.client.post(reverse("cost-list"), payload)
#         exists = Cost.objects.filter(
#             owner=self.user, value=payload["value"], date=payload["date"]
#         ).exists()
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(exists)

#     def test_create_cost_with_negative_value(self):
#         payload = {
#             "value": -200,
#             "date": datetime.date.today().strftime("%Y-%m-%d"),
#             "category": self.category_1.id,
#         }
#         res = self.client.post(reverse("cost-list"), payload)
#         exists = Cost.objects.filter(
#             owner=self.user, value=payload["value"], date=payload["date"]
#         ).exists()
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(exists)

#     def test_retrieve_cost_detail(self):
#         response = self.client.get(reverse("cost-detail", args=[self.cost.id]))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         serializer = CostSerializer(self.cost)
#         print(f"serializer_data: {serializer.data}")
#         print(f"response.data: {response.data}")
#         print()
#         self.assertEqual(response.data, serializer.data)

#     def test_update_cost(self):
#         data = {"value": "200.00", "note": "UpdatedNote"}

#         response = self.client.patch(
#             reverse("cost-detail", args=[self.cost.id]), data=data
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         updated_cost = Cost.objects.get(id=self.cost.id)
#         self.assertEqual(updated_cost.value, 200)
#         self.assertEqual(updated_cost.note, "UpdatedNote")

#     def test_delete_cost(self):
#         response = self.client.delete(reverse("cost-detail", args=[self.cost.id]))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_filter_by_date(self):
#         start_date = datetime.date.today() - datetime.timedelta(days=1)
#         end_date = datetime.date.today() + datetime.timedelta(days=1)
#         res = self.client.get(
#             reverse("cost-by-date"),
#             {
#                 "start_date": start_date.strftime("%Y-%m-%d"),
#                 "end_date": end_date.strftime("%Y-%m-%d"),
#             },
#         )
#         costs = Cost.objects.filter(date__range=[start_date, end_date]).annotate(
#             category_name=F("category__name")
#         )
#         serializer = CostSerializer(costs, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)


# class CategoryTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = USER.objects.create_user(
#             email="test@gmail.com", password="testpassword", username="testuser"
#         )
#         self.category_1 = Category.objects.create(
#             name="test_category_1", owner=self.user
#         )
#         self.category_2 = Category.objects.create(
#             name="test_category_2", owner=self.user
#         )
#         self.cost_1 = Cost.objects.create(
#             value=100,
#             date=datetime.date.today(),
#             owner=self.user,
#             category=self.category_1,
#         )
#         self.cost_2 = Cost.objects.create(
#             value=200,
#             date=datetime.date.today(),
#             owner=self.user,
#             category=self.category_2,
#         )
#         self.client.force_authenticate(user=self.user)

#     def test_list_categories(self):
#         res = self.client.get(reverse("category-list"))
#         categories = Category.objects.filter(owner=self.user).annotate(
#             total_cost=Sum("costs__value")
#         )
#         serializer = CategorySerializer(categories, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)

#     def test_create_category_successful(self):
#         payload = {"name": "test_category_3"}
#         res = self.client.post(reverse("category-list"), payload)
#         exists = Category.objects.filter(owner=self.user, name=payload["name"]).exists()
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(exists)

#     def test_create_category_with_duplicate_name(self):
#         payload = {"name": "test_category_1"}
#         res = self.client.post(reverse("category-list"), payload)
#         exists = Category.objects.filter(owner=self.user, name=payload["name"]).count()
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(exists, 1)

#     def test_retrieve_categories_with_total_cost(self):
#         res = self.client.get(reverse("category-list"))
#         categories = Category.objects.filter(owner=self.user).annotate(
#             total_cost=Sum("costs__value")
#         )
#         serializer = CategorySerializer(categories, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)

import datetime
from django.db.models import Sum, F
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from app.costs.models import Category, Cost
from app.costs.serializers import CategorySerializer, CostSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

USER = get_user_model()


class CostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = USER.objects.create_user(
            email="test@gmail.com", password="testpassword", username="testuser"
        )
        self.category_1 = Category.objects.create(
            name="test_category_1", owner=self.user
        )
        self.cost = Cost.objects.create(
            value=100,
            date=datetime.date.today(),
            owner=self.user,
            category=self.category_1,
        )
        self.client.force_authenticate(user=self.user)

    def test_list_costs(self):
        res = self.client.get(reverse("cost-list"))
        costs = (
            Cost.objects.all()
            .order_by("-date")
            .annotate(category_name=F("category__name"))
        )
        serializer = CostSerializer(costs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_cost_successful(self):
        payload = {
            "value": 200,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "category": self.category_1.id,
        }
        res = self.client.post(reverse("cost-list"), payload)
        exists = Cost.objects.filter(
            owner=self.user,
            value=payload["value"],
            category=payload["category"],
            date=payload["date"],
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_cost_with_invalid_category(self):
        payload = {
            "value": 200,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "category": 99,
        }
        res = self.client.post(reverse("cost-list"), payload)
        exists = Cost.objects.filter(
            owner=self.user, value=payload["value"], date=payload["date"]
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(exists)

    def test_create_cost_with_negative_value(self):
        payload = {
            "value": -200,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "category": self.category_1.id,
        }
        res = self.client.post(reverse("cost-list"), payload)
        exists = Cost.objects.filter(
            owner=self.user, value=payload["value"], date=payload["date"]
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(exists)

    def test_retrieve_cost_detail(self):
        response = self.client.get(reverse("cost-detail", args=[self.cost.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cost.category_name = self.category_1.name
        serializer = CostSerializer(self.cost)
        self.assertEqual(response.data, serializer.data)

    def test_update_cost(self):
        data = {"value": "200.00", "note": "UpdatedNote"}

        response = self.client.patch(
            reverse("cost-detail", args=[self.cost.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_cost = Cost.objects.get(id=self.cost.id)
        self.assertEqual(updated_cost.value, 200)
        self.assertEqual(updated_cost.note, "UpdatedNote")

    def test_delete_cost(self):
        response = self.client.delete(reverse("cost-detail", args=[self.cost.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_by_date(self):
        start_date = datetime.date.today() - datetime.timedelta(days=1)
        end_date = datetime.date.today() + datetime.timedelta(days=1)
        res = self.client.get(
            reverse("cost-by-date"),
            {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
            },
        )
        costs = Cost.objects.filter(date__range=[start_date, end_date]).annotate(
            category_name=F("category__name")
        )
        serializer = CostSerializer(costs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # Additional tests
    def test_create_cost_with_nonexistent_category(self):
        payload = {
            "value": 200,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "category": 99,
        }
        res = self.client.post(reverse("cost-list"), payload)
        exists = Cost.objects.filter(
            owner=self.user, value=payload["value"], date=payload["date"]
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(exists)
        self.assertEqual(
            str(res.data["category"][0]),
            f"“{payload['category']}” is not a valid UUID.",
        )

    def test_validate_value(self):
        with self.assertRaises(ValidationError):
            CostSerializer().validate_value(-1)


class CategoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = USER.objects.create_user(
            email="test@gmail.com", password="testpassword", username="testuser"
        )
        self.category_1 = Category.objects.create(
            name="test_category_1", owner=self.user
        )
        self.category_2 = Category.objects.create(
            name="test_category_2", owner=self.user
        )
        self.cost_1 = Cost.objects.create(
            value=100,
            date=datetime.date.today(),
            owner=self.user,
            category=self.category_1,
        )
        self.cost_2 = Cost.objects.create(
            value=200,
            date=datetime.date.today(),
            owner=self.user,
            category=self.category_2,
        )
        self.client.force_authenticate(user=self.user)

    def test_list_categories(self):
        res = self.client.get(reverse("category-list"))
        categories = Category.objects.filter(owner=self.user).annotate(
            total_cost=Sum("costs__value")
        )
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_category_successful(self):
        payload = {"name": "test_category_3"}
        res = self.client.post(reverse("category-list"), payload)
        exists = Category.objects.filter(owner=self.user, name=payload["name"]).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_category_with_duplicate_name(self):
        payload = {"name": "test_category_1"}
        res = self.client.post(reverse("category-list"), payload)
        exists = Category.objects.filter(owner=self.user, name=payload["name"]).count()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(exists, 1)

    def test_retrieve_categories_with_total_cost(self):
        res = self.client.get(reverse("category-list"))
        categories = Category.objects.filter(owner=self.user).annotate(
            total_cost=Sum("costs__value")
        )
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
