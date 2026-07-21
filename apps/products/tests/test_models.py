import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.products.models import Product
from apps.suppliers.models import Supplier


@pytest.fixture
def supplier():
    return Supplier.objects.create(
        name="ABC Foods",
        country_code="IN",
        active=True,
    )


@pytest.mark.django_db
def test_create_valid_product(supplier):
    product = Product(
        supplier=supplier,
        supplier_sku="SKU001",
        product_name="Basmati Rice",
        pack_size=Decimal("5"),
        unit="kg",
        currency="INR",
        price=Decimal("450"),
    )

    product.full_clean()
    product.save()

    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_negative_price_validation(supplier):
    product = Product(
        supplier=supplier,
        supplier_sku="SKU001",
        product_name="Rice",
        pack_size=Decimal("5"),
        unit="kg",
        currency="INR",
        price=Decimal("-10"),
    )

    with pytest.raises(ValidationError):
        product.full_clean()


@pytest.mark.django_db
def test_zero_pack_size_validation(supplier):
    product = Product(
        supplier=supplier,
        supplier_sku="SKU001",
        product_name="Rice",
        pack_size=Decimal("0"),
        unit="kg",
        currency="INR",
        price=Decimal("100"),
    )

    with pytest.raises(ValidationError):
        product.full_clean()


@pytest.mark.django_db
def test_supplier_sku_unique_per_supplier(supplier):
    Product.objects.create(
        supplier=supplier,
        supplier_sku="SKU001",
        product_name="Rice",
        pack_size=Decimal("5"),
        unit="kg",
        currency="INR",
        price=Decimal("100"),
    )

    with pytest.raises(IntegrityError):
        Product.objects.create(
            supplier=supplier,
            supplier_sku="SKU001",
            product_name="Rice Premium",
            pack_size=Decimal("10"),
            unit="kg",
            currency="INR",
            price=Decimal("200"),
        )


@pytest.mark.django_db
def test_same_supplier_sku_allowed_for_different_suppliers(supplier):
    supplier2 = Supplier.objects.create(
        name="XYZ Foods",
        country_code="US",
        active=True,
    )

    Product.objects.create(
        supplier=supplier,
        supplier_sku="SKU001",
        product_name="Rice",
        pack_size=Decimal("5"),
        unit="kg",
        currency="INR",
        price=Decimal("100"),
    )

    Product.objects.create(
        supplier=supplier2,
        supplier_sku="SKU001",
        product_name="Rice",
        pack_size=Decimal("5"),
        unit="kg",
        currency="USD",
        price=Decimal("100"),
    )

    assert Product.objects.count() == 2