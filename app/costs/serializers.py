from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from app.costs import models


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_cost = serializers.DecimalField(
        max_digits=11, decimal_places=2, allow_null=True, read_only=True
    )

    class Meta:
        model = models.Category
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "total_cost",
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=models.Category.objects.all(), fields=["owner", "name"]
            )
        ]


class CostSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_name = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = models.Cost
        fields = [
            "id",
            "owner",
            "category",
            "category_name",
            "value",
            "date",
            "created_at",
            "note",
        ]

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("This field must be an positive number.")
        return value

    def validate_category(self, category):
        if category.owner != self.context["request"].user:
            raise serializers.ValidationError(
                "This category does not belong to this user."
            )
        return category
