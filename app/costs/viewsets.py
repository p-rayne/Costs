from django.db import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

# from django_filters.rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from app.costs import serializers
from app.costs.models import Cost, Category
from app.costs.filters import IsOwnerFilterBackend, CostFilter


class CostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CostSerializer
    queryset = Cost.objects.all()
    filter_backends = [
        IsOwnerFilterBackend,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = CostFilter
    permission_classes = [IsAuthenticated]
    ordering_fields = ["date", "value"]
    ordering = ["-date"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            self.serializer_class = serializers.ListRetrieveCategorySerializer
        else:
            self.serializer_class = serializers.CreateUpdateDeleteCategorySerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        if self.action in ["list", "retrieve"]:
            queryset = Category.objects.filter(owner=user).annotate(
                total_spent=models.Sum(models.F("costs__value"))
            )
        else:
            queryset = Category.objects.filter(owner=user)
        return queryset
