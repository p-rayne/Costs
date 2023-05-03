from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from .models import Cost


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CostFilter(filters.FilterSet):
    """
    FilterSet for the Cost model. Allows for filtering by category and date range.
    """

    category = CharFilterInFilter(
        field_name="category__name",
        lookup_expr="in",
        help_text="Category name to filter by",
    )
    date = filters.DateRangeFilter(
        field_name="date",
        help_text="Value used for filtering by time period: today, week, month, year.",
    )

    class Meta:
        model = Cost
        fields = ["category", "date"]


class OrderingFilterWithSchema(OrderingFilter):
    def get_schema_fields(self, view):
        self.ordering_description = "Fields for sorting: " + ", ".join(
            view.ordering_fields
        )
        return super().get_schema_fields(view)
