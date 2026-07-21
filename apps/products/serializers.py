"""Serializers for Product model.

Includes supplier_name as a read-only field to avoid extra queries in clients.
"""
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    supplier_name = serializers.CharField(
        source="supplier.name",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "supplier",
            "supplier_name",
            "supplier_sku",
            "product_name",
            "pack_size",
            "unit",
            "currency",
            "price",
            "imported_at",
        )