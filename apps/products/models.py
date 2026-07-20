from django.db import models

from apps.common.choices import CurrencyChoices, UnitChoices
from apps.suppliers.models import Supplier


class Product(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="products",
    )

    supplier_sku = models.CharField(max_length=100)

    product_name = models.CharField(max_length=255)

    pack_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    unit = models.CharField(
        max_length=10,
        choices=UnitChoices.choices,
    )

    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        db_index=True,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"

        constraints = [
            models.UniqueConstraint(
                fields=["supplier", "supplier_sku"],
                name="uq_supplier_supplier_sku",
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="ck_product_price_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(pack_size__gt=0),
                name="ck_product_pack_size_positive",
            ),
        ]