"""Serializers for import endpoints.

Validates uploaded files and simple request-level checks.
"""
from rest_framework import serializers


class ProductCSVImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, file):
        if not file.name.lower().endswith(".csv"):
            raise serializers.ValidationError(
                "Only CSV files are allowed."
            )

        return file