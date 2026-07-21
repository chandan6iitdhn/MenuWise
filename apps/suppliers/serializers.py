"""Serializers for Supplier model.

Defines how Supplier objects are serialized over the API.
"""
from rest_framework import serializers

from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = (
            "id",
            "name",
            "country_code",
            "active",
            "created_at",
        )