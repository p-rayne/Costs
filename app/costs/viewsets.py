from django.db.models import Sum, F
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.costs import serializers
from app.costs.models import Cost, Category
from app.costs.filters import CostFilter, OrderingFilterWithSchema


class CostViewSet(viewsets.ModelViewSet):
    """
    An API endpoint that allows costs to be viewed or edited.
    """

    serializer_class = serializers.CostSerializer
    queryset = Cost.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilterWithSchema,
    ]
    filterset_class = CostFilter
    permission_classes = [IsAuthenticated]
    ordering_fields = ["date", "value"]
    ordering = ["-date"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cost.objects.none()
        return self.queryset.filter(owner=self.request.user).annotate(
            category_name=F("category__name")
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description="Start date in format: YYYY-MM-DD",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description="End date in format: YYYY-MM-DD",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    @action(detail=False, methods=["GET"], filter_backends=[])
    def by_date(self, request):
        """
        Retrieve costs by date range.
        """

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not (start_date and end_date):
            return Response({"error": "Please provide start_date and end_date"})

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        queryset = self.get_queryset().filter(date__range=(start_date, end_date))
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    An API endpoint that allows the category to be viewed or edited.
    """

    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Category.objects.none()
        queryset = self.queryset.filter(owner=self.request.user).annotate(
            total_cost=Sum("costs__value")
        )
        return queryset
