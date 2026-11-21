"""
Data Loader — reads CSV files from data/ and hydrates typed dataclass instances.
Directly parses dotkey_products.csv and india_cosmetics_brands_market_intel.csv
for competitors, reviews, and customer acquisition intelligence.
"""

from __future__ import annotations

import csv
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..models import (
    BrandMarketIntel,
    CompetitorProduct,
    Platform,
    Product,
    Review,
    SentimentLabel,
)

logger = logging.getLogger(__name__)

# Resolve data/ directory relative to project root
_DATA_DIR = Path(__file__).resolve().parents[2] / "data"

_PLATFORM_MAP: dict[str, Platform] = {p.value: p for p in Platform}
_SENTIMENT_MAP: dict[str, SentimentLabel] = {s.value: s for s in SentimentLabel}


def _split(value: str, sep: str = "|") -> list[str]:
    """Split a pipe- or comma-separated cell into a list, stripping whitespace."""
    if not value:
        return []
    return [v.strip() for v in value.split(sep) if v.strip()]


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes")


def _parse_date(value: str) -> Optional[datetime]:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%d/%m/%Y"):
        try:
            return datetime.strptime(value.strip()[:19], "%Y-%m-%dT%H:%M:%S" if "T" in value else "%Y-%m-%d")
        except ValueError:
            continue
    return None


def _csv_rows(filename: str) -> list[dict[str, str]]:
    """Read a CSV file with utf-8-sig to handle optional BOM."""
    path = _DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Load Dot & Key Products (Shopify-extracted catalog)
# ---------------------------------------------------------------------------

def load_dotkey_products() -> list[Product]:
    """Load Dot & Key products from data/dotkey_products.csv (Shopify format)."""
    products: list[Product] = []
    for row in _csv_rows("dotkey_products.csv"):
        try:
            price_str = row.get("prices_inr", "0").split("|")[0].strip()
            price_val = float(price_str) if price_str else 0.0

            sizes_str = row.get("sizes", "")
            size_match = re.search(r"(\d+(?:\.\d+)?)", sizes_str)
            size_val = float(size_match.group(1)) if size_match else 50.0

            tags_list = _split(row.get("tags", ""), "|")

            ingredients = [
                t.replace("fltr_ingredients_", "").replace("st_ingredients_", "").title()
                for t in tags_list
                if "ingredients_" in t
            ]
            concerns = [
                t.replace("fltr_skin_concern_", "").replace("st_skinconcern_", "").replace("skinconcern_", "").title()
                for t in tags_list
                if "concern" in t
            ]
            skin_types = [
                t.replace("fltr_skin_type_", "").replace("st_skin_type_", "").replace("skintype_", "").title()
                for t in tags_list
                if "skin_type" in t or "skintype_" in t
            ]

            title = row.get("title", "").strip()
            category = row.get("product_type", "").strip() or "Skincare"

            products.append(
                Product(
                    id=str(row.get("id", "")).strip(),
                    name=title,
                    category=category,
                    subcategory=row.get("handle", "").strip(),
                    description=row.get("description", "").strip(),
                    ingredients=ingredients or ["Fruit Actives", "Vitamin Complex"],
                    key_benefits=[f"Hydrating {category}", "Non-greasy finish", "Made for Indian skin"],
                    skin_type=skin_types or ["All Skin Types"],
                    concerns=concerns or ["Dullness", "Hydration"],
                    price_inr=price_val,
                    size_ml=size_val,
                    image_urls=_split(row.get("image_urls", ""), "|"),
                    product_url=f"https://dotandkey.com/products/{row.get('handle', '').strip()}",
                    is_active=True,
                    launched_date=_parse_date(row.get("published_at", "")),
                    tags=tags_list,
                )
            )
        except Exception as exc:
            logger.warning("Skipping product row %r: %s", row.get("id"), exc)

    logger.info("Loaded %d Dot & Key products.", len(products))
    return products


# ---------------------------------------------------------------------------
# Load Market Intelligence (india_cosmetics_brands_market_intel.csv)
# ---------------------------------------------------------------------------

def load_market_intel() -> list[BrandMarketIntel]:
    """Load 100 brand records from data/india_cosmetics_brands_market_intel.csv."""
    intel_records: list[BrandMarketIntel] = []
    for row in _csv_rows("india_cosmetics_brands_market_intel.csv"):
        try:
            pinfo = row.get("product_info", "")
            parts = [p.strip() for p in pinfo.split("|")]
            brand = parts[0] if len(parts) > 0 else ""
            category = parts[1] if len(parts) > 1 else ""
            flagship = [x.strip() for x in parts[2].split(",")] if len(parts) > 2 else []
            price_band = parts[3] if len(parts) > 3 else ""

            prices = re.findall(r"\d+", price_band)
            min_price = float(prices[0]) if len(prices) > 0 else 200.0
            max_price = float(prices[1]) if len(prices) > 1 else 1000.0

            reviews_str = row.get("customer_reviews", "")
            pos_match = re.search(r"Pos:\s*([^|]+)", reviews_str)
            neg_match = re.search(r"Neg:\s*(.+)", reviews_str)
            pos_list = [p.strip() for p in pos_match.group(1).split(",")] if pos_match else []
            neg_list = [n.strip() for n in neg_match.group(1).split(",")] if neg_match else []

            competitors = [c.strip() for c in row.get("competitors", "").split(",") if c.strip()]
            opportunities = [o.strip() for o in row.get("market_opportunities", "").split(";") if o.strip()]

            intel_records.append(
                BrandMarketIntel(
                    brand=brand,
                    category=category,
                    flagship_lines=flagship,
                    price_band=price_band,
                    min_price=min_price,
                    max_price=max_price,
                    positive_sentiment=pos_list,
                    negative_friction=neg_list,
                    competitors=competitors,
                    market_opportunities=opportunities,
                )
            )
        except Exception as exc:
            logger.warning("Skipping market intel row: %s", exc)

    logger.info("Loaded %d brand market intel records.", len(intel_records))
    return intel_records


# ---------------------------------------------------------------------------
# Derive Competitor Products & Reviews from Market Intel
# ---------------------------------------------------------------------------

def load_competitor_products() -> list[CompetitorProduct]:
    """
    Derive benchmark competitor products from data/india_cosmetics_brands_market_intel.csv.
    Generates structured CompetitorProduct instances for all major brands.
    """
    competitors: list[CompetitorProduct] = []
    intel_records = load_market_intel()

    for brand_intel in intel_records:
        if brand_intel.brand.lower() in ("dot & key", "dot and key"):
            continue

        avg_price = (brand_intel.min_price + brand_intel.max_price) / 2.0
        for item in brand_intel.flagship_lines[:3]:
            cat = "Skincare"
            subcat = "General"
            item_lower = item.lower()
            if "sun" in item_lower:
                cat = "Sunscreen"
                subcat = "Hydrating"
            elif "serum" in item_lower or "c" in item_lower or "niacinamide" in item_lower or "retinol" in item_lower:
                cat = "Serum"
                subcat = "Actives"
            elif "wash" in item_lower or "cleanser" in item_lower:
                cat = "Face Wash"
                subcat = "Cleansing"
            elif "cream" in item_lower or "moistur" in item_lower or "gel" in item_lower or "lotion" in item_lower:
                cat = "Moisturizer"
                subcat = "Barrier Repair"

            competitors.append(
                CompetitorProduct(
                    brand=brand_intel.brand,
                    product_name=f"{brand_intel.brand} {item}",
                    category=cat,
                    subcategory=subcat,
                    price_inr=avg_price,
                    size_ml=50.0,
                    rating=4.3,
                    review_count=8500,
                    platform=Platform.AMAZON,
                    ingredients=["Clinical Actives", "Botanical Extracts"],
                    key_claims=brand_intel.positive_sentiment[:3],
                    availability=True,
                )
            )

    logger.info("Synthesized %d competitor products from market intel.", len(competitors))
    return competitors


def load_reviews() -> list[Review]:
    """
    Synthesize reviews from data/india_cosmetics_brands_market_intel.csv
    transforming 'Pos:' and 'Neg:' feedback into structured Review records.
    """
    reviews: list[Review] = []
    intel_records = load_market_intel()

    for brand_intel in intel_records:
        for idx, pos_phrase in enumerate(brand_intel.positive_sentiment):
            reviews.append(
                Review(
                    product_id=brand_intel.brand,
                    platform=Platform.AMAZON,
                    rating=5 if idx == 0 else 4,
                    title=f"Great experience with {brand_intel.brand}",
                    text=f"I really loved this: {pos_phrase}. Worked nicely on my Indian skin.",
                    verified_purchase=True,
                    sentiment=SentimentLabel.POSITIVE,
                    sentiment_score=0.85,
                    key_phrases=[pos_phrase],
                    topics=["effectiveness", "texture", "value"],
                )
            )

        for neg_phrase in brand_intel.negative_friction:
            reviews.append(
                Review(
                    product_id=brand_intel.brand,
                    platform=Platform.AMAZON,
                    rating=2,
                    title=f"Disappointed with {brand_intel.brand}",
                    text=f"Had an issue with this product: {neg_phrase}. Needs formulation improvement.",
                    verified_purchase=True,
                    sentiment=SentimentLabel.NEGATIVE,
                    sentiment_score=-0.65,
                    key_phrases=[neg_phrase],
                    topics=["fragrance", "gentleness", "packaging"],
                )
            )

    logger.info("Synthesized %d reviews from market intel.", len(reviews))
    return reviews


# ---------------------------------------------------------------------------
# Module singletons
# ---------------------------------------------------------------------------

SAMPLE_DOTKEY_PRODUCTS = load_dotkey_products()
SAMPLE_MARKET_INTEL = load_market_intel()
SAMPLE_COMPETITOR_PRODUCTS = load_competitor_products()
SAMPLE_REVIEWS = load_reviews()
SAMPLE_COMPETITOR_BRANDS = sorted({c.brand for c in SAMPLE_COMPETITOR_PRODUCTS})
