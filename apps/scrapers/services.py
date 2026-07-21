import requests
from bs4 import BeautifulSoup


class SupplierScraperService:

    def scrape(self, url):
        html = self._fetch_html(url)
        rows = self._parse_html(html)

        return rows

    def _fetch_html(self, url):
        response = requests.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        return response.text

    def _parse_html(self, html):
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table")

        if table is None:
            raise ValueError("No table found.")

        rows = []

        for tr in table.find_all("tr")[1:]:
            cols = [
                td.get_text(strip=True)
                for td in tr.find_all("td")
            ]

            rows.append({
                "supplier_sku": cols[0],
                "product_name": cols[1],
                "pack_size": cols[2],
                "unit": cols[3],
                "currency": cols[4],
                "price": cols[5],
            })

        return rows