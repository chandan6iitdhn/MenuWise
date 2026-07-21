import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):

    supplier = django_filters.NumberFilter(
        field_name="supplier_id"
    )

    currency = django_filters.CharFilter()

    active_supplier = django_filters.BooleanFilter(
        field_name="supplier__active"
    )

    class Meta:
        model = Product
        fields = [
            "supplier",
            "currency",
            "active_supplier",
        ]