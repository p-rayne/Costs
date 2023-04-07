from django_filters import rest_framework as filters

from .models import Cost


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CostFilter(filters.FilterSet):
    category = CharFilterInFilter(field_name="category__name", lookup_expr="in")
    date = filters.DateRangeFilter(field_name="date")

    class Meta:
        model = Cost
        fields = ["category", "date"]
