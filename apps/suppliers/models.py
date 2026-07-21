"""Supplier model and metadata.

Contains Supplier model fields used across the app:
- name
- country_code
- active
- created_at

Used by Product and other modules to associate supplier data.
"""
from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "suppliers"
        ordering = ["name"]

    def __str__(self):
        return self.name