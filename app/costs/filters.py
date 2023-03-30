from rest_framework.filters import BaseFilterBackend
from django_filters import rest_framework as filters

from .models import Cost


class IsOwnerFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CostFilter(filters.FilterSet):
    category = CharFilterInFilter(field_name="category__name", lookup_expr="in")
    date = filters.DateRangeFilter(field_name="date")

    class Meta:
        model = Cost
        fields = ["category", "date"]
