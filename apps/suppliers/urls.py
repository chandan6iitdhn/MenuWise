from django.urls import path

from .views import SupplierListAPIView

urlpatterns = [
    path(
        "",
        SupplierListAPIView.as_view(),
        name="supplier-list",
    ),
]