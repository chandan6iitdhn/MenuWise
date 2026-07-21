from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from apps.products.models import Product
from apps.suppliers.models import Supplier


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def setup_products():
    supplier1 = Supplier.objects.create(
        name="ABC Foods",
        country_code="IN",
        active=True,
    )

    supplier2 = Supplier.objects.create(
        name="XYZ Foods",
        country_code="US",
        active=False,
    )

    product1 = Product.objects.create(
        supplier=supplier1,
        supplier_sku="SKU001",
        product_name="Basmati Rice",
        pack_size=Decimal("5"),
        unit="kg",
        currency="INR",
        price=Decimal("450"),
    )

    product2 = Product.objects.create(
        supplier=supplier2,
        supplier_sku="SKU002",
        product_name="Olive Oil",
        pack_size=Decimal("1"),
        unit="l",
        currency="USD",
        price=Decimal("15"),
    )

    return {
        "supplier1": supplier1,
        "supplier2": supplier2,
        "product1": product1,
        "product2": product2,
    }


@pytest.mark.django_db
def test_list_products(api_client, setup_products):
    response = api_client.get("/api/v1/products/")

    assert response.status_code == 200
    assert response.data["count"] == 2


@pytest.mark.django_db
def test_filter_by_supplier(api_client, setup_products):
    supplier = setup_products["supplier1"]

    response = api_client.get(
        "/api/v1/products/",
        {"supplier": supplier.id},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["supplier"] == supplier.id


@pytest.mark.django_db
def test_filter_by_currency(api_client, setup_products):
    response = api_client.get(
        "/api/v1/products/",
        {"currency": "USD"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["currency"] == "USD"


@pytest.mark.django_db
def test_filter_by_active_supplier(api_client, setup_products):
    response = api_client.get(
        "/api/v1/products/",
        {"active_supplier": True},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_search_product(api_client, setup_products):
    response = api_client.get(
        "/api/v1/products/",
        {"search": "Rice"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["product_name"] == "Basmati Rice"


@pytest.mark.django_db
def test_product_detail(api_client, setup_products):
    product = setup_products["product1"]

    response = api_client.get(
        f"/api/v1/products/{product.id}/"
    )

    assert response.status_code == 200
    assert response.data["id"] == product.id