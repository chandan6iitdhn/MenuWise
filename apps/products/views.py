from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    """
    GET /api/v1/products/

    Supports:
    - Pagination
    - Filter by supplier
    - Filter by currency
    - Filter by active supplier
    - Search by product_name
    """

    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_class = ProductFilter
    search_fields = ("product_name",)

    def get_queryset(self):
        return (
            Product.objects
            .select_related("supplier")
            .all()
        )


class ProductRetrieveAPIView(RetrieveAPIView):
    """
    GET /api/v1/products/<id>/
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        return (
            Product.objects
            .select_related("supplier")
            .all()
        )