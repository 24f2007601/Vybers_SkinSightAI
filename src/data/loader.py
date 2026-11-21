"""
Data Loader — reads CSV files from data/ and returns typed dataclass instances.
All modules should import SAMPLE_* constants via this loader instead of models.py.
"""

from __future__ import annotations

import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..models import (
    CompetitorProduct,
    Platform,
    Product,
    Review,
    SentimentLabel,
)

logger = logging.getLogger(__name__)

# Resolve data/ directory relative to the project root (two levels up from src/data/)
_DATA_DIR = Path(__file__).resolve().parents[2] / "data"

_PLATFORM_MAP: dict[str, Platform] = {p.value: p for p in Platform}
_SENTIMENT_MAP: dict[str, SentimentLabel] = {s.value: s for s in SentimentLabel}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _split(value: str, sep: str = "|") -> list[str]:
    """Split a pipe-separated cell into a list, stripping whitespace."""
    return [v.strip() for v in value.split(sep) if v.strip()] if value else []


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes")


def _parse_date(value: str) -> Optional[datetime]:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y"):
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    logger.warning("Unrecognised date format: %r", value)
    return None


def _csv_rows(filename: str) -> list[dict[str, str]]:
    """Read a CSV file and return a list of row dicts."""
    path = _DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Data file not found: {path}. "
            "Run the project from its root directory or check that data/ is present."
        )
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Public loaders
# ---------------------------------------------------------------------------

def load_dotkey_products() -> list[Product]:
    """Load Dot & Key products from data/dotkey_products.csv."""
    products: list[Product] = []
    for row in _csv_rows("dotkey_products.csv"):
        try:
            products.append(
                Product(
                    id=row["id"].strip(),
                    name=row["name"].strip(),
                    category=row["category"].strip(),
                    subcategory=row["subcategory"].strip(),
                    description=row["description"].strip(),
                    ingredients=_split(row["ingredients"]),
                    key_benefits=_split(row["key_benefits"]),
                    skin_type=_split(row["skin_type"]),
                    concerns=_split(row["concerns"]),
                    price_inr=float(row["price_inr"]),
                    size_ml=float(row["size_ml"]),
                    image_urls=_split(row["image_urls"]),
                    product_url=row["product_url"].strip(),
                    is_active=_parse_bool(row.get("is_active", "True")),
                    launched_date=_parse_date(row.get("launched_date", "")),
                    tags=_split(row.get("tags", "")),
                )
            )
        except (KeyError, ValueError) as exc:
            logger.warning("Skipping malformed product row %r: %s", row, exc)
    logger.info("Loaded %d Dot & Key products from CSV.", len(products))
    return products


def load_competitor_products() -> list[CompetitorProduct]:
    """Load competitor products from data/competitor_products.csv."""
    competitors: list[CompetitorProduct] = []
    for row in _csv_rows("competitor_products.csv"):
        try:
            platform_value = row.get("platform", "amazon").strip().lower()
            platform = _PLATFORM_MAP.get(platform_value, Platform.AMAZON)
            competitors.append(
                CompetitorProduct(
                    brand=row["brand"].strip(),
                    product_name=row["product_name"].strip(),
                    category=row["category"].strip(),
                    subcategory=row["subcategory"].strip(),
                    price_inr=float(row["price_inr"]),
                    size_ml=float(row["size_ml"]),
                    rating=float(row["rating"]),
                    review_count=int(row["review_count"]),
                    platform=platform,
                    product_url=row.get("product_url", "").strip(),
                    ingredients=_split(row["ingredients"]),
                    key_claims=_split(row["key_claims"]),
                    availability=_parse_bool(row.get("availability", "True")),
                )
            )
        except (KeyError, ValueError) as exc:
            logger.warning("Skipping malformed competitor row %r: %s", row, exc)
    logger.info("Loaded %d competitor products from CSV.", len(competitors))
    return competitors


def load_reviews() -> list[Review]:
    """Load customer reviews from data/reviews.csv."""
    reviews: list[Review] = []
    for row in _csv_rows("reviews.csv"):
        try:
            platform_value = row.get("platform", "amazon").strip().lower()
            platform = _PLATFORM_MAP.get(platform_value, Platform.AMAZON)

            sentiment_value = row.get("sentiment", "").strip().lower()
            sentiment = _sentiment_MAP_safe(sentiment_value)

            reviews.append(
                Review(
                    product_id=row["product_id"].strip(),
                    platform=platform,
                    rating=int(row["rating"]),
                    title=row["title"].strip(),
                    text=row["text"].strip(),
                    verified_purchase=_parse_bool(row.get("verified_purchase", "False")),
                    helpful_votes=int(row.get("helpful_votes", 0)),
                    sentiment=sentiment,
                    sentiment_score=float(row.get("sentiment_score", 0.0)),
                    key_phrases=_split(row.get("key_phrases", "")),
                    topics=_split(row.get("topics", "")),
                )
            )
        except (KeyError, ValueError) as exc:
            logger.warning("Skipping malformed review row %r: %s", row, exc)
    logger.info("Loaded %d reviews from CSV.", len(reviews))
    return reviews


def _sentiment_MAP_safe(value: str) -> Optional[SentimentLabel]:
    if not value:
        return None
    return _SENTIMENT_MAP.get(value)


# ---------------------------------------------------------------------------
# Module-level singletons — loaded once, reused everywhere
# ---------------------------------------------------------------------------

def _lazy_load():
    """Load all datasets once and cache them as module-level attributes."""
    global SAMPLE_DOTKEY_PRODUCTS, SAMPLE_COMPETITOR_PRODUCTS, SAMPLE_REVIEWS
    global SAMPLE_COMPETITOR_BRANDS

    SAMPLE_DOTKEY_PRODUCTS = load_dotkey_products()
    SAMPLE_COMPETITOR_PRODUCTS = load_competitor_products()
    SAMPLE_REVIEWS = load_reviews()
    SAMPLE_COMPETITOR_BRANDS = sorted(
        {c.brand for c in SAMPLE_COMPETITOR_PRODUCTS}
    )


# Initialise on import
SAMPLE_DOTKEY_PRODUCTS: list[Product] = []
SAMPLE_COMPETITOR_PRODUCTS: list[CompetitorProduct] = []
SAMPLE_REVIEWS: list[Review] = []
SAMPLE_COMPETITOR_BRANDS: list[str] = []

try:
    _lazy_load()
except FileNotFoundError as _e:
    logger.error(
        "Could not load data CSVs (%s). "
        "SAMPLE_* lists will be empty until data/ is accessible.",
        _e,
    )
