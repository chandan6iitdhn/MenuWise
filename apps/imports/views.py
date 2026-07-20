from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductCSVImportSerializer
from .services import ProductImportService


class ProductCSVImportAPIView(APIView):

    def post(self, request):
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