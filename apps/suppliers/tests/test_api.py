import pytest
from rest_framework.test import APIClient

from apps.suppliers.models import Supplier


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_list_suppliers(api_client):
    Supplier.objects.create(
        name="ABC Foods",
        country_code="IN",
    )

    Supplier.objects.create(
        name="XYZ Foods",
        country_code="US",
    )

    response = api_client.get("/api/v1/suppliers/")

    assert response.status_code == 200
    assert response.data["count"] == 2