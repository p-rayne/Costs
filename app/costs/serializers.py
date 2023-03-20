from rest_framework import serializers
from costs import models


class FilterCategoryListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        # serializer = self.parent.parent.__class__(value, context=self.context)
        serializer = CategorySerializer(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCategoryListSerializer
        model = models.Category
        fields = ["id", "url", "owner", "name", "description", "children"]


class CostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all()
    )
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = models.Cost
        fields = [
            "url",
            "id",
            "owner",
            "category",
            "value",
            "date",
            "created_at",
            "note",
        ]
