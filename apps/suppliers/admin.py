from django.contrib import admin

from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "country_code",
        "active",
        "created_at",
    )

    search_fields = (
        "name",
        "country_code",
    )

    list_filter = (
        "active",
        "country_code",
    )

    ordering = (
        "name",
    )

    list_per_page = 25

    readonly_fields = (
        "created_at",
    )