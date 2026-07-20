from django.urls import path

from .views import ProductCSVImportAPIView

urlpatterns = [
    path(
        "products/",
        ProductCSVImportAPIView.as_view(),
        name="product-import",
    ),
]