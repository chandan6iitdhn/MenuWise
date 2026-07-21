import io

import pytest

from apps.imports.services import ProductImportService
from apps.products.models import Product
from apps.suppliers.models import Supplier


@pytest.mark.django_db
def test_import_valid_csv():
    supplier = Supplier.objects.create(
        name="ABC Foods",
        country_code="IN",
    )

    csv_data = f"""supplier_id,supplier_sku,product_name,pack_size,unit,currency,price
{supplier.id},SKU001,Rice,5,kg,INR,100
"""

    service = ProductImportService()

    result = service.import_products(
        io.StringIO(csv_data)
    )

    assert result["imported"] == 1
    assert result["failed"] == 0
    assert result["duplicates"] == 0
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_invalid_headers():
    csv_data = """sku,name
1,Rice
"""

    service = ProductImportService()

    with pytest.raises(ValueError):
        service.import_products(
            io.StringIO(csv_data)
        )


@pytest.mark.django_db
def test_duplicate_product_is_skipped():
    supplier = Supplier.objects.create(
        name="ABC Foods",
        country_code="IN",
    )

    Product.objects.create(
        supplier=supplier,
        supplier_sku="SKU001",
        product_name="Rice",
        pack_size=5,
        unit="kg",
        currency="INR",
        price=100,
    )

    csv_data = f"""supplier_id,supplier_sku,product_name,pack_size,unit,currency,price
{supplier.id},SKU001,Rice,5,kg,INR,100
"""

    service = ProductImportService()

    result = service.import_products(
        io.StringIO(csv_data)
    )

    assert result["duplicates"] == 1
    assert result["imported"] == 0
    assert result["failed"] == 0
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_default_currency_for_indian_supplier():
    supplier = Supplier.objects.create(
        name="ABC Foods",
        country_code="IN",
    )

    csv_data = f"""supplier_id,supplier_sku,product_name,pack_size,unit,currency,price
{supplier.id},SKU001,Rice,5,kg,,100
"""

    service = ProductImportService()

    result = service.import_products(
        io.StringIO(csv_data)
    )

    assert result["imported"] == 1

    product = Product.objects.first()

    assert product.currency == "INR"


@pytest.mark.django_db
def test_default_currency_for_non_indian_supplier():
    supplier = Supplier.objects.create(
        name="US Foods",
        country_code="US",
    )

    csv_data = f"""supplier_id,supplier_sku,product_name,pack_size,unit,currency,price
{supplier.id},SKU001,Rice,5,kg,,100
"""

    service = ProductImportService()

    result = service.import_products(
        io.StringIO(csv_data)
    )

    assert result["imported"] == 1

    product = Product.objects.first()

    assert product.currency == "USD"


@pytest.mark.django_db
def test_negative_price_is_skipped():
    supplier = Supplier.objects.create(
        name="ABC Foods",
        country_code="IN",
    )

    csv_data = f"""supplier_id,supplier_sku,product_name,pack_size,unit,currency,price
{supplier.id},SKU001,Rice,5,kg,INR,-10
"""

    service = ProductImportService()

    result = service.import_products(
        io.StringIO(csv_data)
    )

    assert result["failed"] == 1
    assert result["imported"] == 0
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_unknown_supplier_is_skipped():
    csv_data = """supplier_id,supplier_sku,product_name,pack_size,unit,currency,price
999,SKU001,Rice,5,kg,INR,100
"""

    service = ProductImportService()

    result = service.import_products(
        io.StringIO(csv_data)
    )

    assert result["failed"] == 1
    assert result["imported"] == 0
    assert Product.objects.count() == 0