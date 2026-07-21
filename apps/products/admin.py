"""Django admin configuration for Product model.

Provides search, filters, list display and select_related optimization to
make product management efficient in the admin UI.
"""
from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "supplier",
        "supplier_sku",
        "product_name",
        "pack_size",
        "unit",
        "currency",
        "price",
        "imported_at",
    )

    search_fields = (
        "supplier_sku",
        "product_name",
        "supplier__name",
    )

    list_filter = (
        "currency",
        "unit",
        "supplier",
        "supplier__active",
    )

    autocomplete_fields = (
        "supplier",
    )

    list_select_related = (
        "supplier",
    )

    ordering = (
        "supplier",
        "product_name",
    )

    list_per_page = 25

    readonly_fields = (
        "imported_at",
    )