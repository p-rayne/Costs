from django.db import models
from django.contrib.auth.models import User

import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name="categories", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )

    def __str__(self):
        return self.name


class Cost(models.Model):
    RUBLE = "RUB"
    DOLLAR = "USD"
    EURO = "EUR"
    LIRA = "TRY"
    TENGE = "KZT"
    CURRENCY_CHOICES = [
        (RUBLE, "Рубль"),
        (DOLLAR, "Доллар"),
        (EURO, "Евро"),
        (LIRA, "Лира"),
        (TENGE, "Тенге"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name="costs", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="costs", on_delete=models.CASCADE
    )
    value = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default=RUBLE,
    )
