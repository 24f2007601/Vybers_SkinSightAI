import logging
import asyncio
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from ..models import Product
from ..data.loader import SAMPLE_DOTKEY_PRODUCTS

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_CATALOG_CRAWL_LINKS = 20


class DotKeyCatalogExtractor:
    """Extracts Dot & Key product catalog from official website or data/ CSV."""

    BASE_URL: str = "https://dotkey.in"
    PRODUCTS_URL: str = "https://dotkey.in/collections/all"

    def __init__(self, use_sample_data: bool = True) -> None:
        self.use_sample_data = use_sample_data
        self._client: Optional[httpx.AsyncClient] = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT_SECONDS, follow_redirects=True)
        return self._client

    async def aclose(self) -> None:
        """Explicit lifecycle cleanup for the HTTP client."""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def extract_all_products(self) -> list[Product]:
        """Extract all products from Dot & Key website or CSV cache."""
        if self.use_sample_data:
            return SAMPLE_DOTKEY_PRODUCTS

        client = self._get_client()
        products: list[Product] = []
        try:
            response = await client.get(self.PRODUCTS_URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            product_links = self._extract_product_links(soup)

            for link in product_links[:MAX_CATALOG_CRAWL_LINKS]:
                product = await self._extract_product(link)
                if product:
                    products.append(product)
        except Exception as exc:
            logger.warning("Error extracting live catalog from %s: %s", self.PRODUCTS_URL, exc)
            return SAMPLE_DOTKEY_PRODUCTS
        finally:
            await self.aclose()

        return products or SAMPLE_DOTKEY_PRODUCTS

    def _extract_product_links(self, soup: BeautifulSoup) -> list[str]:
        """Extract unique product URLs from collection page."""
        links: set[str] = set()
        for item in soup.select(".product-grid-item a, .grid-view-item a, .product-card a"):
            href = item.get("href")
            if href and "/products/" in href:
                links.add(urljoin(self.BASE_URL, href))
        return list(links)

    async def _extract_product(self, url: str) -> Optional[Product]:
        """Extract single product details from HTML."""
        client = self._get_client()
        try:
            response = await client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            product_data = self._extract_json_ld(soup) or self._extract_from_meta(soup)

            if not product_data:
                return None

            raw_price = float(product_data.get("price", 0))
            price_inr = raw_price / 100.0 if raw_price > 1000 else raw_price

            return Product(
                name=product_data.get("name", "").strip(),
                description=product_data.get("description", "").strip(),
                price_inr=price_inr,
                product_url=url,
                image_urls=product_data.get("images", []),
            )
        except Exception as exc:
            logger.debug("Failed parsing product from %s: %s", url, exc)
            return None

    def _extract_json_ld(self, soup: BeautifulSoup) -> Optional[dict]:
        """Extract product structured metadata from JSON-LD blocks."""
        import json
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("@type") == "Product":
                            return self._parse_schema_org_product(item)
                elif isinstance(data, dict) and data.get("@type") == "Product":
                    return self._parse_schema_org_product(data)
            except Exception:
                continue
        return None

    def _parse_schema_org_product(self, data: dict) -> dict:
        """Parse standard schema.org/Product JSON-LD."""
        offers = data.get("offers", {})
        price = 0.0
        if isinstance(offers, dict):
            price = offers.get("price", 0.0)
        elif isinstance(offers, list) and offers:
            price = offers[0].get("price", 0.0)

        images = data.get("image", [])
        if isinstance(images, str):
            images = [images]

        return {
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "price": price,
            "images": images,
        }

    def _extract_from_meta(self, soup: BeautifulSoup) -> Optional[dict]:
        """Fallback to OpenGraph meta tags."""
        name = soup.find("meta", property="og:title")
        desc = soup.find("meta", property="og:description")
        image = soup.find("meta", property="og:image")
        price = soup.find("meta", property="product:price:amount")

        if not name:
            return None

        return {
            "name": name.get("content", ""),
            "description": desc.get("content", "") if desc else "",
            "price": float(price.get("content", 0.0)) if price else 0.0,
            "images": [image.get("content")] if image and image.get("content") else [],
        }
