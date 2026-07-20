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