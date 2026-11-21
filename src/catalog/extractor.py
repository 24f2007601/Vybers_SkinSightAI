"""
Product Catalog Extractor for Dot & Key
Extracts product information from Dot & Key website and structures it
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from ..models import Product, SAMPLE_DOTKEY_PRODUCTS


class DotKeyCatalogExtractor:
    """Extracts Dot & Key product catalog from website"""

    BASE_URL = "https://dotkey.in"
    PRODUCTS_URL = "https://dotkey.in/collections/all"

    def __init__(self, use_sample_data: bool = True):
        self.use_sample_data = use_sample_data
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)

    async def extract_all_products(self) -> list[Product]:
        """Extract all products from Dot & Key website"""
        if self.use_sample_data:
            return SAMPLE_DOTKEY_PRODUCTS

        products = []
        try:
            # Get collection page
            response = await self.client.get(self.PRODUCTS_URL)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find product links
            product_links = self._extract_product_links(soup)

            # Extract each product
            for link in product_links[:20]:  # Limit for demo
                product = await self._extract_product(link)
                if product:
                    products.append(product)

        except Exception as e:
            print(f"Error extracting catalog: {e}")
            # Fallback to sample data
            return SAMPLE_DOTKEY_PRODUCTS
        finally:
            await self.client.aclose()

        return products

    def _extract_product_links(self, soup: BeautifulSoup) -> list[str]:
        """Extract product URLs from collection page"""
        links = []
        # Look for product grid items
        for item in soup.select('.product-grid-item a, .grid-view-item a, .product-card a'):
            href = item.get('href')
            if href and '/products/' in href:
                full_url = urljoin(self.BASE_URL, href)
                links.append(full_url)
        return list(set(links))  # Deduplicate

    async def _extract_product(self, url: str) -> Optional[Product]:
        """Extract single product details"""
        try:
            response = await self.client.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract product data from JSON-LD or meta tags
            product_data = self._extract_json_ld(soup)
            if not product_data:
                product_data = self._extract_from_meta(soup)

            if not product_data:
                return None

            return Product(
                name=product_data.get('name', ''),
                description=product_data.get('description', ''),
                price_inr=float(product_data.get('price', 0)) / 100,  # Convert from paise
                product_url=url,
                image_urls=product_data.get('images', []),
                # Additional fields would be parsed from description/page
            )
        except Exception as e:
            print(f"Error extracting product {url}: {e}")
            return None

    def _extract_json_ld(self, soup: BeautifulSoup) -> Optional[dict]:
        """Extract product data from JSON-LD structured data"""
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Product':
                            return self._parse_schema_org_product(item)
                elif data.get('@type') == 'Product':
                    return self._parse_schema_org_product(data)
            except:
                continue
        return None

    def _parse_schema_org_product(self, data: dict) -> dict:
        """Parse Schema.org Product format"""
        return {
            'name': data.get('name', ''),
            'description': data.get('description', ''),
            'price': data.get('offers', {}).get('price', 0),
            'images': data.get('image', []) if isinstance(data.get('image'), list) else [data.get('image', '')],
        }

    def _extract_from_meta(self, soup: BeautifulSoup) -> Optional[dict]:
        """Extract from Open Graph / Twitter meta tags"""
        og_data = {}
        for meta in soup.find_all('meta'):
            prop = meta.get('property') or meta.get('name')
            content = meta.get('content')
            if prop and content:
                if prop.startswith('og:'):
                    og_data[prop[3:]] = content
                elif prop.startswith('twitter:'):
                    og_data[prop[8:]] = content

        if og_data.get('title'):
            return {
                'name': og_data.get('title', ''),
                'description': og_data.get('description', ''),
                'images': [og_data.get('image', '')] if og_data.get('image') else [],
            }
        return None


async def main():
    extractor = DotKeyCatalogExtractor(use_sample_data=True)
    products = await extractor.extract_all_products()
    print(f"Extracted {len(products)} products")
    for p in products:
        print(f"  - {p.name} ({p.category}) - ₹{p.price_inr}")


if __name__ == "__main__":
    asyncio.run(main())