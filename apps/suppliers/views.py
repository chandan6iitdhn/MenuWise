"""API views for supplier-related endpoints.

Provides supplier list endpoint. Keep views thin; business logic
belongs in serializers/services.
"""
from rest_framework.generics import ListAPIView

from .models import Supplier
from .serializers import SupplierSerializer


class SupplierListAPIView(ListAPIView):
    """
    GET /api/v1/suppliers/
    """

    serializer_class = SupplierSerializer

    def get_queryset(self):
        return Supplier.objects.all()