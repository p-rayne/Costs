from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid


class Category(models.Model):
    """
    Cost categories
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name="categories", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Cost(models.Model):
    """
    Costs
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        User, related_name="costs", on_delete=models.CASCADE, db_index=True
    )
    category = models.ForeignKey(
        Category, related_name="costs", on_delete=models.CASCADE, db_index=True
    )
    value = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField(db_index=True)
    created_at = models.DateField(auto_now_add=True)
    note = models.CharField(max_length=255, null=True, blank=True)


@receiver(post_save, sender=User)
def create_default_category(sender, instance, created, **kwargs):
    """
    Creates default categories for a new user
    """

    DEFAULT_CATEGORY = (
        ("Продукты", "Расходы на еду"),
        ("Транспорт", "Расходы на транспорт"),
        ("Развлечения", "Расходы на развлечения"),
        ("Коммунальные платежи", "Расходы на коммунальные платежи"),
    )
    if created:
        category = [
            Category(owner=instance, name=name, description=description)
            for name, description in DEFAULT_CATEGORY
        ]

        Category.objects.bulk_create(category)
