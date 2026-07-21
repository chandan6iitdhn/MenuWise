"""Management command to scrape supplier product pages.

Usage: manage.py scrape_supplier <url>
Delegates scraping to SupplierScraperService and reports counts.
"""
from django.core.management.base import BaseCommand

from apps.scrapers.services import SupplierScraperService


class Command(BaseCommand):
    help = "Scrape supplier products"

    def add_arguments(self, parser):
        parser.add_argument(
            "url",
            type=str,
        )

    def handle(self, *args, **options):
        scraper = SupplierScraperService()

        rows = scraper.scrape(
            options["url"]
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Found {len(rows)} products."
            )
        )