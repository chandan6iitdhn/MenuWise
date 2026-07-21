"""API views for supplier-related endpoints.

Provides supplier list endpoint. Keep views thin; business logic
belongs in serializers/services.
"""
import logging

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Supplier
from .serializers import SupplierSerializer

logger = logging.getLogger(__name__)


class SupplierListAPIView(ListCreateAPIView):
    """
    GET /api/v1/suppliers/
    POST /api/v1/suppliers/  Creates a new supplier

    The POST endpoint validates input using SupplierSerializer and returns
    a JSON representation of the newly created supplier including its id.
    """

    serializer_class = SupplierSerializer

    def get_queryset(self):
        return Supplier.objects.all()

    def create(self, request, *args, **kwargs):
        """Create a new Supplier and return its serialized representation.

        Accepts JSON body with fields: name, country_code, active (optional).
        Returns 201 with the created supplier data or a generic error response.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except Exception as e:
            logger.exception("Error creating Supplier: %s", e)
            return Response(
                {"detail": f"Internal server error. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)