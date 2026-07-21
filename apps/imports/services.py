import csv
from decimal import Decimal, InvalidOperation

from apps.products.models import Product
from apps.suppliers.models import Supplier
from apps.common.choices import CurrencyChoices, UnitChoices
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


class ProductImportService:
    BULK_INSERT_BATCH_SIZE = 1000

    EXPECTED_HEADERS = [
        "supplier_id",
        "supplier_sku",
        "product_name",
        "pack_size",
        "unit",
        "currency",
        "price",
    ]

    UNIT_MAPPING = {
        "gram": "g",
        "grams": "g",
        "g": "g",

        "kg": "kg",
        "kgs": "kg",
        "kilogram": "kg",
        "kilograms": "kg",

        "ml": "ml",
        "milliliter": "ml",
        "millilitre": "ml",

        "l": "l",
        "liter": "l",
        "litre": "l",
        "ltr": "l",

        "piece": "each",
        "pieces": "each",
        "pc": "each",
        "pcs": "each",
        "each": "each",
    }

    def import_products(self, csv_file):
        try:
            logger.info("starting product import")
            reader = self._parse_csv(csv_file)

            self._validate_headers(reader.fieldnames)

            rows = list(reader)
            suppliers = self._load_suppliers(rows)
            existing_products = self._load_existing_products(suppliers.keys())

            products = []
            errors = []
            duplicates = 0
            seen_products = set()

            for row_number, row in enumerate(rows, start=2):

                row = self._normalize_row(row)

                row_errors = self._validate_row(row)

                if row_errors:
                    errors.append({
                        "row": row_number,
                        "errors": row_errors,
                    })
                    continue

                supplier = suppliers.get(int(row["supplier_id"]))

                if supplier is None:
                    errors.append({
                        "row": row_number,
                        "errors": {
                            "supplier_id": "Supplier not found."
                        }
                    })
                    continue

                key = (
                    supplier.id,
                    row["supplier_sku"],
                )

                if key in existing_products:
                    duplicates += 1
                    continue

                if key in seen_products:
                    duplicates += 1
                    continue
                seen_products.add(key)

                product = self._build_product(
                    row,
                    supplier,
                )

                products.append(product)

            if products:
                with transaction.atomic():
                    Product.objects.bulk_create(products, batch_size=self.BULK_INSERT_BATCH_SIZE)

            total_rows = len(rows)
            imported_products = len(products)
            total_errors = len(errors)

            logger.info("import completed. Imported=%s Failed=%s Duplicates=%s",
                        imported_products, total_errors, duplicates)

            return {
                "total_rows": total_rows,
                "imported": imported_products,
                "duplicates": duplicates,
                "failed": total_errors,
                "errors": errors,
            }

        except Exception as e:
            logger.exception("Unexpected error during product import: %s", e)
            raise

    def _parse_csv(self, csv_file):
        content = csv_file.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        return csv.DictReader(content.splitlines())

    def _validate_headers(self, headers):
        if headers != self.EXPECTED_HEADERS:
            raise ValueError(
                f"Invalid CSV headers. Expected: {self.EXPECTED_HEADERS}"
            )

    def _normalize_row(self, row):
        normalized = {}

        for key, value in row.items():
            normalized[key] = value.strip() if value else ""

        normalized["unit"] = self.UNIT_MAPPING.get(
            normalized["unit"].lower(),
            normalized["unit"].lower(),
        )

        normalized["currency"] = normalized["currency"].upper()

        return normalized

    def _get_default_currency(self, supplier):
        if supplier.country_code.upper() == "IN":
            return CurrencyChoices.INR

        return CurrencyChoices.USD

    def _validate_row(self, row):

        errors = {}

        if not row["supplier_sku"]:
            errors["supplier_sku"] = "Supplier SKU is required."

        if not row["product_name"]:
            errors["product_name"] = "Product name is required."

        try:
            price = Decimal(row["price"])

            if price < 0:
                errors["price"] = "Price cannot be negative."

        except (InvalidOperation, ValueError):
            errors["price"] = "Invalid price."

        try:
            pack_size = Decimal(row["pack_size"])

            if pack_size <= 0:
                errors["pack_size"] = "Pack size must be greater than zero."

        except (InvalidOperation, ValueError):
            errors["pack_size"] = "Invalid pack size."

        if row["unit"] not in UnitChoices.values:
            errors["unit"] = "Invalid unit."

        if row["currency"] and row["currency"] not in CurrencyChoices.values:
            errors["currency"] = "Invalid currency."

        return errors

    def _load_suppliers(self, rows):

        supplier_ids = {
            int(row["supplier_id"])
            for row in rows
            if row.get("supplier_id")
        }

        return Supplier.objects.in_bulk(supplier_ids)

    def _load_existing_products(self, supplier_ids):

        return {
            (
                product.supplier_id,
                product.supplier_sku,
            )
            for product in Product.objects.filter(
                supplier_id__in=supplier_ids
            ).only(
                "supplier_id",
                "supplier_sku",
            )
        }

    def _build_product(self, row, supplier):

        currency = row["currency"]

        if not currency:
            currency = self._get_default_currency(supplier)

        return Product(
            supplier=supplier,
            supplier_sku=row["supplier_sku"],
            product_name=row["product_name"],
            pack_size=Decimal(row["pack_size"]),
            unit=row["unit"],
            currency=currency,
            price=Decimal(row["price"]),
        )