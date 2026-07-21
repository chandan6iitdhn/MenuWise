"""Shared enumerations for units and currencies.

Defines canonical UnitChoices and CurrencyChoices used by Product and
import normalization logic. Keep values stable to avoid data drift.
"""
from django.db import models


class UnitChoices(models.TextChoices):
    GRAM = "g", "Gram"
    KILOGRAM = "kg", "Kilogram"
    MILLILITER = "ml", "Milliliter"
    LITER = "l", "Liter"
    EACH = "each", "Each"


class CurrencyChoices(models.TextChoices):
    INR = "INR", "Indian Rupee"
    USD = "USD", "US Dollar"