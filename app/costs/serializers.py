from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from app.costs import models


class FilterCategoryPKRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context["request"].user
        queryset = models.Category.objects.filter(owner=user)
        return queryset


class CostsCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Cost
        fields = ["url", "value", "date"]


class ListRetrieveCategorySerializer(serializers.HyperlinkedModelSerializer):
    costs = CostsCategorySerializer(many=True)
    total_spent = serializers.DecimalField(
        max_digits=11, decimal_places=2, allow_null=True
    )

    class Meta:
        model = models.Category
        fields = [
            "id",
            "url",
            "name",
            "description",
            "total_spent",
            "costs",
        ]


class CreateUpdateDeleteCategorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Category
        fields = ["id", "url", "owner", "name", "description"]

        validators = [
            UniqueTogetherValidator(
                queryset=models.Category.objects.all(), fields=["owner", "name"]
            )
        ]


class CostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = FilterCategoryPKRelatedField()
    category_name = serializers.ReadOnlyField(source="category.name")
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = models.Cost
        fields = [
            "url",
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
