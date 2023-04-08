from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from app.costs import models


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model. Includes the owner, name, description, and total cost of the category.

    Attributes:
        owner: The owner of the category. Defaults to the current user.
        total_cost: The total cost of the category.
    """

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
    """
    Serializer for the Cost model. Includes the owner, category, value, date, and note of the cost.

    Attributes:
        owner: The owner of the cost. Defaults to the current user.
        category_name: The name of the category associated with the cost.
        created_at: The date the cost was created.
    """

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
        """
        Validates that the value field is a positive number.
        """
        if value < 0:
            raise serializers.ValidationError("This field must be an positive number.")
        return value

    def validate_category(self, category):
        """
        Validates that the category belongs to the current user.
        """
        if category.owner != self.context["request"].user:
            raise serializers.ValidationError(
                "This category does not belong to this user."
            )
        return category
