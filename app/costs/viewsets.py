from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.costs import serializers
from app.costs.models import Cost
from app.costs.filters import IsOwnerFilterBackend


class CostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CostSerializer
    queryset = Cost.objects.all()
    filter_backends = [IsOwnerFilterBackend]
    permission_classes = [IsAuthenticated]
    ordering_fields = ["date"]
