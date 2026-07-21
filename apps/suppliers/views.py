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