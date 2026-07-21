"""CSV import API views.

Endpoint accepts a CSV file, validates payload via a serializer and
delegates heavy lifting to ProductImportService.
"""
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductCSVImportSerializer
from .services import ProductImportService

logger = logging.getLogger(__name__)


class ProductCSVImportAPIView(APIView):

    def post(self, request):
        try:
            serializer = ProductCSVImportSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            service = ProductImportService()

            result = service.import_products(
                serializer.validated_data["file"]
            )

            return Response(
                result,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.exception("Error importing products: %s", e)
            return Response(
                {"detail": f"Internal server error. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )